import React, { useState, useRef } from "react";
import { ReactMic } from "react-mic";

const SpeechToText = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const websocketRef = useRef(null);

  const startRecording = () => {
    setIsRecording(true);

    // Initialize WebSocket connection
    websocketRef.current = new WebSocket("ws://localhost:6188/visualize/");

    websocketRef.current.onopen = () => {
      console.log("WebSocket connection opened");
    };

    websocketRef.current.onmessage = (event) => {
      // Receive transcription text from the server
      const message = event.data;
      setTranscript((prev) => prev + "\n" + message);
    };

    websocketRef.current.onclose = () => {
      console.log("WebSocket connection closed");
    };
  };

  const stopRecording = () => {
    setIsRecording(false);

    // Close WebSocket connection
    if (websocketRef.current) {
      websocketRef.current.close();
    }
  };

  const onData = (recordedBlob) => {
    if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
      // Send audio data to WebSocket server as a blob
      websocketRef.current.send(recordedBlob.blob);
    }
  };

  const handleMouseDown = () => {
    // User presses the button, start recording
    startRecording();
  };

  const handleMouseUp = () => {
    // User releases the button, stop recording
    stopRecording();
  };

  return (
    <div>
      <h2>Speech to Text</h2>
      <div>
        <button
          onMouseDown={handleMouseDown}
          onMouseUp={handleMouseUp}
          onTouchStart={handleMouseDown}  // For touch devices
          onTouchEnd={handleMouseUp}      // For touch devices
          className="record-button"
        >
          Hold to Record
        </button>
      </div>
      <ReactMic
        record={isRecording}
        className="sound-wave"
        onStop={stopRecording}
        onData={onData}
        strokeColor="#000000"
        backgroundColor="#FF4081"
        mimeType="audio/wav"
      />
      <div>
        <h3>Transcription:</h3>
        <pre>{transcript}</pre>
      </div>
    </div>
  );
};

export default SpeechToText;


