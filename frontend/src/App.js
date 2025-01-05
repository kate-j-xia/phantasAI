import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Home from './components/Home';
import Images from './components/Images';
import Prompts from './components/Prompts'
import Transcripts from './components/Transcripts'
import './styles/App.css';

const App = () => {
    return (
      <BrowserRouter>
        <div className="app">
          <Sidebar />
          <div className="content">
            
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/transcripts" element={<Transcripts />} />
              <Route path="/prompts" element={<Prompts />} />
              <Route path="/images" element={<Images />} />
            </Routes>
            
          </div>
        </div>        
      </BrowserRouter>
    );
  };
  
export default App;


