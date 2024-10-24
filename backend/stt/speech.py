import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
import queue
import vosk
import sys
import json
import numpy as np
from pathlib import Path
import wave
import sys
import os
import time
from fastapi import WebSocket
import tempfile

data_to_write = ["Line 1", "Line 2", "Line 3"]

def save_data():
    with open('output_file.txt', 'w') as file:
        for line in data_to_write:
            file.write(line + '\n')

def get_model_path():
    current_dir = Path(__file__).resolve().parent
    print(f'main(): current path = {current_dir}')

    model_path = current_dir.parent / 'models' / 'vosk-model-en-us-0.22'
    print(f'main(): model path = {model_path}')
    return str(model_path)

async def from_file(audio_path: str):
    vosk.SetLogLevel(0)

    model = vosk.Model(model_path=get_model_path())        
    
    """ 
    # Save the file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:       
        tmp.write(await audio_file.read())  # Write the file contents to the temp file
        tmp_path = tmp.name
    """
    # Check file size and path for debugging
    print(f"from_file(): audio file at {audio_path}, size: {os.path.getsize(audio_path)} bytes")       
    
    try:    
        # Ensure the file is a valid WAV file
        with wave.open(audio_path, "rb") as wf:
            if wf.getnchannels() != 1:                
                err = "Audio file must be mono"
                return {"status": 400, "err": err}
            if wf.getsampwidth() != 2:
                err = "Audio file must have a sample width of 16-bit"
                return {"status": 400, "err": err}
            if wf.getframerate() != 16000:
                err = "Audio file must have a sample rate of 16kHz"
                return {"status": 400, "err": err} 

            print(f"File has {wf.getnchannels()} channels, "
                    f"{wf.getsampwidth()} bytes per sample, "
                    f"and {wf.getframerate()} frame rate")
             # Initialize the recognizer
            recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

            # Process the audio and perform speech-to-text
            transcription = ""
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    transcription += result

            # Get the final partial transcription (if any)
            transcription += recognizer.FinalResult()
            print(f'from_file(): transcription = {transcription}')
            prompt = json.loads(transcription)
            print(f'from_file(): prompt = {prompt}')

        # Return the transcription as JSON
        return {"status": 200, "prompt": prompt["text"]}

    except wave.Error as we:
        print(f'from_file(): wave file error - {we}') 

        return {"status": 400, "err": we}
    finally:
        # Clean up by removing the temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)               

    # Convert the file to a standard WAV format using pydub
    # audio = await AudioSegment.from_wav(audio_file)
    # print(f'from_file(): from audioSegment()')
    # converted_path = tmp_path.replace(".wav", "_converted.wav")    
    # audio.export(converted_path, format="wav")
    # print(f'from_file(): converted to temp file')

    # Open the temp file with soundfile to get the audio data and samplerate
    # audio_data, samplerate = await sf.read(audio_file)
    # sf.write(tmp_path, audio_data, samplerate)

    # wf = wave.open("test.wav", "rb")
    # wf = wave.open(audio_file, "rb")
    # if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    #     print("Audio file must be WAV format mono PCM.")
    #     sys.exit(1)

    """
    rec.SetWords(True)
    rec.SetPartialWords(True)
    while True:
        data = audio_data.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
    """

    # print(f'from_file(): results = {result}')
    # Clean up the temp file
    # os.remove(tmp_path)
    # os.remove(converted_path)
    #return {200, result}

# Initialize a queue to hold audio data
q = queue.Queue()

# Threshold parameters for silence detection
SILENCE_THRESHOLD = 3  # Adjust based on microphone sensitivity
SILENCE_DURATION = 6.5   # Time in seconds to consider as "silence" before stopping

# Callback function to stream audio data into the queue
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))  # Put the recorded data into the queue

# Function to calculate the energy level (volume) of the audio
def get_audio_energy(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.linalg.norm(audio_data) / len(audio_data)  # RMS energy of audio

# Function to recognize speech using Vosk
def recognize_speech(model, samplerate) -> str:
    rec = vosk.KaldiRecognizer(model, samplerate)
    last_audio_time = time.time()
    
    while True:
        data = q.get()
        energy = get_audio_energy(data)

        # If energy level is high, treat it as speech; otherwise, check for silence
        if energy > SILENCE_THRESHOLD:
            last_audio_time = time.time()  # Reset timer
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print(f"Recognized Text: {result.get('text', '')}")
            else:
                partial_result = json.loads(rec.PartialResult())
                print(f"Partial Result: {partial_result.get('partial', '')}")
        else:
            # Check if the silence duration has passed
            if time.time() - last_audio_time > SILENCE_DURATION:
                print("End of speech detected, stopping...")
                break
    print(f'recognize_speech(): final results = {rec.FinalResult()}')
    return rec


def from_stream():
    model = vosk.Model(get_model_path())

    samplerate = 16000  # Vosk models typically use 16000 Hz sample rate
    device = None  # Use default input device

    # Open the audio stream
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=callback):
        print("Listening from streaming...\nSTART talking clearly and loud enough - \
              if you pause more than 5 seconds, it will consider you finish talking!")
        recognize_speech(model, samplerate)
    # return result

# Initialize a queue to hold audio data
audio_queue = queue.Queue()

# handle speech recognition with Vosk
def speech_to_text(websocket: WebSocket, model, samplerate: int):
    rec = vosk.KaldiRecognizer(model, samplerate)
    
    while True:
        try:
            # Receive audio data in small chunks
            audio_data = audio_queue.get()
            if rec.AcceptWaveform(audio_data):
                result = json.loads(rec.Result())
                # Send the transcribed text to the client
                websocket.send_text(f"Recognized Text: {result.get('text', '')}")
            else:
                partial_result = json.loads(rec.PartialResult())
                websocket.send_text(f"Partial Result: {partial_result.get('partial', '')}")
        except Exception as e:
            print(f"Error: {e}")
            break

# Main program
if __name__ == "__main__":
    print(f'Transcribing from speech....')   
    # from_file()
    from_stream()
    print(f'*** DONE ***')   



