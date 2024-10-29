import React, { useState, useRef } from "react";
import { ReactMic } from "react-mic";

const SpeechToText = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("")
  const [imageStatus, setImageStatus] = useState("")

  const startRecording = () => {
    setIsRecording(true);
  };

  const stopRecording = async (recordedBlob) => {
    setIsRecording(false);
    console.log("stopRecording(): Recorded Blob:", recordedBlob); 

    if (recordedBlob && recordedBlob.blob) {
        // Send the recorded audio to the FastAPI backend
        const formData = new FormData();
        // const audioBlob = new Blob(recordedBlob.blob, { type: 'audio/wav' });
        // const url = URL.createObjectURL(recordedBlob.blobUrl);
        // setSrc(url) //setting the url in your state. A hook in this case btw
        const wavBlob = await blobToWav16kHz(recordedBlob.blob);  // Convert to WAV
        formData.append("file", wavBlob, "prompt.wav");
        for (let pair of formData.entries()) {
            console.log("stopRecording(): " + pair[0] + ':', pair[1]);  // This should show the "file" and Blob
        }
        
        fetch("http://0.0.0.0:6188/visualize/", {
            method: "POST",
            body: formData,
        })
        .then((response) => response.json())
        .then((data) => {
            // Set the returned transcript
            console.log("stopRecording(): got response.data = ", data)
            console.log("stopRecording(): got results = ", data.message)
            setTranscript(data.message["prompt"]);
            setSummary(data.message["summary"])
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }
  };

  const blobToWav16kHz = async (blob) => {
    const arrayBuffer = await blob.arrayBuffer();
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  
    // Decode the audio data
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
  
    // Resample the audio buffer to 16kHz
    const offlineContext = new OfflineAudioContext(
      audioBuffer.numberOfChannels,
      Math.ceil(audioBuffer.duration * 16000), // Duration * sample rate
      16000  // 16kHz
    );
  
    // Copy the audio buffer into the offline context
    const source = offlineContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(offlineContext.destination);
    source.start();
  
    // Render the new audio buffer at 16kHz
    const renderedBuffer = await offlineContext.startRendering();
  
    // Convert the audio buffer to a WAV Blob
    const wavBuffer = audioBufferToWav(renderedBuffer);
    return new Blob([wavBuffer], { type: "audio/wav" });
  };

  const blobToWav = async (blob) => {
    const arrayBuffer = await blob.arrayBuffer();
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
  
    const wavBuffer = audioBufferToWav(audioBuffer);
    return new Blob([wavBuffer], { type: "audio/wav" });
  };
  
  // Helper function to convert AudioBuffer to WAV format
  const audioBufferToWav = (buffer) => {
    let numOfChan = buffer.numberOfChannels,
        length = buffer.length * numOfChan * 2 + 44,
        bufferArray = new ArrayBuffer(length),
        view = new DataView(bufferArray),
        channels = [],
        i, sample,
        offset = 0,
        pos = 0;
  
    setUint32(0x46464952); // "RIFF"
    setUint32(length - 8); // file length - 8
    setUint32(0x45564157); // "WAVE"
  
    setUint32(0x20746d66); // "fmt " chunk
    setUint32(16); // length = 16
    setUint16(1); // PCM (uncompressed)
    setUint16(numOfChan);
    setUint32(buffer.sampleRate);
    setUint32(buffer.sampleRate * 2 * numOfChan); // avg. bytes/sec
    setUint16(numOfChan * 2); // block-align
    setUint16(16); // 16-bit (hardcoded in this demo)
  
    setUint32(0x61746164); // "data" - chunk
    setUint32(length - pos - 4); // chunk length
  
    // Write interleaved data
    for (i = 0; i < buffer.numberOfChannels; i++)
      channels.push(buffer.getChannelData(i));
  
    while (pos < length) {
      for (i = 0; i < numOfChan; i++) {
        sample = Math.max(-1, Math.min(1, channels[i][offset])); // clamp
        sample = (sample < 0 ? sample * 0x8000 : sample * 0x7FFF) | 0; // scale to 16-bit signed int
        view.setInt16(pos, sample, true); // write 16-bit sample
        pos += 2;
      }
      offset++; // next source sample
    }
  
    function setUint16(data) {
      view.setUint16(pos, data, true);
      pos += 2;
    }
  
    function setUint32(data) {
      view.setUint32(pos, data, true);
      pos += 4;
    }
  
    return bufferArray;
  };
  
  return (
    <div>
      <h2>Speech to Text</h2>
      <div>
        <button
          onMouseDown={startRecording}
          onMouseUp={stopRecording}
          onTouchStart={startRecording}
          onTouchEnd={stopRecording}
          className="record-button"
        >
          Hold to Speak
        </button>
      </div>
      <ReactMic
        record={isRecording}
        className="sound-wave"
        onStop={stopRecording}
        strokeColor="#000000"
        backgroundColor="#FF4081"
        mimeType="audio/wav"    
      />
      <div>
        <h3>Transcript:</h3>
        <pre>{transcript}</pre>
      </div>
      <div>
        <h3>Summary:</h3>
        <pre>{summary}</pre>
      </div>
      <div>
        <h3>Image Status:</h3>
        <pre>{imageStatus}</pre>
      </div>
    </div>
  );
};

export default SpeechToText;

