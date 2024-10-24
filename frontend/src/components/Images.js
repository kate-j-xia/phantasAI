import React from 'react';

function Files() {
  const files = ['File1.txt', 'File2.jpg', 'File3.pdf'];

  return (
    <div>
      <h1>Files Page</h1>
      <ul>
        {files.map((file, index) => (
          <li key={index}>{file}</li>
        ))}
      </ul>
    </div>
  );
}

export default Files;

