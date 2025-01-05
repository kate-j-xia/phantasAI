import React, { useState, useEffect }  from "react";
import "../styles/Images.css";

const Images = () => {
    const [expandedRows, setExpandedRows] = useState([]);

    const data = [
        { timestamp: "2024-12-04 12:00", 
            prompt: "Short snippet of text for file1. Click to expand for more details.",
            filename: "file1.pdf", status: "Uploaded", size: "1.2 MB" },
        { timestamp: "2024-12-04 12:05", 
            prompt: "Short snippet of text for file1. Click to expand for more details.",
            filename: "file2.docx", status: "Processing", size: "2.1 MB" },
        { timestamp: "2024-12-04 12:10", 
            prompt: "Short snippet of text for file1. Click to expand for more details.",
            filename: "file3.jpg", status: "Failed", size: "3.0 MB" },
    ];

    const toggleExpand = (index) => {
        setExpandedRows((prev) =>
        prev.includes(index)
            ? prev.filter((i) => i !== index)
            : [...prev, index]
        );
    };

    return (
        <div className="parent-container">
            <div className="title">Ideas</div>
            <table>
                <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Prompt</th>
                    <th>Image</th>
                    <th>Status</th>
                    <th>Size</th>
                    <th className="checkbox-column">Like</th>
                </tr>
                </thead>
                <tbody>
                {data.map((row, index) => (
                    <tr key={index}>
                    <td>{row.timestamp}</td>
                    <td>
                        <div
                        className={`prompt-column ${
                            expandedRows.includes(index) ? "expanded" : ""
                        }`}
                        onClick={() => toggleExpand(index)}
                        >
                        {expandedRows.includes(index)
                            ? `${row.prompt} This is the full expanded paragraph for more context.`
                            : row.prompt}
                        </div>
                        <span
                        className="toggle-text"
                        onClick={() => toggleExpand(index)}
                        >
                        {expandedRows.includes(index) ? "Show Less" : "Show More"}
                        </span>
                    </td>
                    <td>
                        <a href={`/${row.filename}`} className="link">
                        {row.filename}
                        </a>
                    </td>
                    <td>{row.status}</td>
                    <td>{row.size}</td>
                    <td className="checkbox-column">
                        <input type="checkbox" />
                    </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
};

export default Images;
