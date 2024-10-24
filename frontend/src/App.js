import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Home from './components/Home';
import Images from './components/Images';
import Recording from './components/Recording'
import './styles/App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/Prompts" element={<Recording />} />
            <Route path="/Images" element={<Images />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;


