import React, { useEffect, useState } from 'react';

import '../styles/Home.css';

function Home() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [prompt, setPrompt] = useState('');
    const [input2, setInput2] = useState('');

    const handleSubmit = async () => {
        setLoading(true);
        setResult(null); // Reset result if any
        try {
            const response = await fetch("https://localhost:6188/visualize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    prompt: prompt,
                    input2: input2
                }),
            });
            const data = await response.json();
            setResult(data); // Set result to data if request is successful
        } catch (error) {
            console.error("Error fetching data:", error);
            setResult({ error: "Failed to fetch data" });
        } finally {
            setLoading(false); // Stop loading once request completes
        }
    };

    return (
        <div className="parent-container">     
            <div className="title">Visualize</div>       
            <div className="container">                
                <textarea className="input-textarea"
                    type="text"
                    placeholder="Enter your prompt"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    disabled={loading}
                />                       
                <button className="button-gradient"
                        onClick={handleSubmit} 
                        disabled={loading}>
                    {loading ? 'Loading...' : 'Generate'}
                </button>                
            </div>
            <div>
                {loading && (
                    <div className="spinner"></div>
                )}
                {result && !loading && (
                    <div className="result">
                        <h3>Result:</h3>
                        <pre>{JSON.stringify(result, null, 2)}</pre>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Home;

function Simple() {

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
        <p>Welcome to the Aph Artist Land</p>
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

// export default Simple;

