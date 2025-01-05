import React, { useState } from 'react';
import { Link } from 'react-router-dom';


import hamburgerIcon from "../assets/icons8-hamburger-menu.svg";
import snailLogo from "../assets/snail-logo.png"

import paletteIcon from "../assets/artist-palette.png"
import trascribeIcon from "../assets/live-transcribe.svg"
import imageIcon from "../assets/icons8-image-48.png"

import '../styles/Sidebar.css';

function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className={`sidebar ${isCollapsed ? "collapsed" : ""}`}>
        <button className="hamburger-button" onClick={toggleSidebar}>
          <img
            src={hamburgerIcon} alt="Toggle Sidebar"
          />
        </button>
        {!isCollapsed && (
            <div className="sidebar-header">
                <img src={snailLogo} alt="Aph-artist Logo"/>
                <span>Aph-artist.ai</span>
            </div>)
        }
        <ul className="menu">
            <li>
                <a href="/">
                    <img src={paletteIcon} alt="Visualization" className="menu-icon" />
                    {!isCollapsed && <span>Visualization</span>}
                </a>
            </li>
            <li>
                <a href="/transcripts">
                    <img src={trascribeIcon} alt="Transcribe" className="menu-icon" />
                    {!isCollapsed && <span>Transcription</span>}
                </a>
            </li>
            <li>
                <a href="/images">
                    <img src={imageIcon} alt="Images" className="menu-icon" />
                    {!isCollapsed && <span>Images</span>}
                </a>
            </li>
        </ul>    
    </div>
  );
}

export default Sidebar;


