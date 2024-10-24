import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Sidebar.css';

function Sidebar() {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleMenu = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Menu</h2>
        <button onClick={toggleMenu}>
          {isExpanded ? 'Collapse' : 'Expand'}
        </button>
      </div>
      <nav className={`menu ${isExpanded ? 'expanded' : ''}`}>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/prompts">Prompts</Link></li>
          <li><Link to="/images">Images</Link></li>
          
        </ul>
      </nav>
    </div>
  );
}

export default Sidebar;


