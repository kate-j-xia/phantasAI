import React, { useEffect, useState } from 'react';

function Home() {

    const [file, setFile] = useState(null);
    const [prompt, setPrompt] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append("file", file);
        formData.append("prompt", prompt);
        
        const response = await fetch('/visualize/', {
            method: 'POST',
            body: formData,
        });
        
        const data = await response.json();
        alert(data.message);
    };
  
    return (
        <div>
        <h1>Home Page</h1>
        <p>Welcome to the simple React UI with a sidebar menu.</p>
        <form className="form" onSubmit={handleSubmit}>
            <label htmlFor="title">Title:</label>
            <input type="text" id="title" name="title" placeholder="Enter a title for your art" />

            <label htmlFor="prompt">Prompt:</label>
            <textarea id="prompt" name="prompt" placeholder="Speak clearly about your idea"></textarea>

            <button type="submit">Submit</button>
        </form>
        </div>
    );
}

export default Home;

