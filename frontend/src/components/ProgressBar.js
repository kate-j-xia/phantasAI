import React, { useState, useEffect } from "react";
import "../styles/ProgressBar.css";

const ProgressBar = ({ show, onComplete }) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (show) {
      setProgress(0); // Reset progress when the progress bar is shown
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval);
            onComplete(); // Notify parent component that the progress is complete
            return 100;
          }
          return prev + 2;
        });
      }, 300);

      return () => clearInterval(interval); // Cleanup on component unmount
    }
  }, [show, onComplete]);

  if (!show) return null; // Hide the progress bar when `show` is false

  return (
    <div className="progress-container">
      <div className="progress-bar" style={{ width: `${progress}%` }} />
      <div className="progress-label">{progress}%</div>
    </div>
  );
};

export default ProgressBar;
