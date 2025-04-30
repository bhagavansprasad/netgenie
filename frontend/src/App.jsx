// src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import Dashboard from './components/dashboard';
import CreateTemplate from './components/CreateTemplate';
import ConfigurationPage from './components/ConfigurationPage';
import CreateDevicePage from './components/CreateDevicePage';
import CreateCustomerPage from './components/CreateCustomerPage';
import GenerateConfigurationsPage from './components/GenerateConfigurationsPage';
import './App.css'; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/create-template" element={<CreateTemplate />} />{/* Add the new route */}
        <Route path="/configurations" element={<ConfigurationPage />} />
        <Route path="/new-device" element={<CreateDevicePage />} />
        <Route path="/new-customer" element={<CreateCustomerPage />} />
        <Route path="/generate-configurations" element={<GenerateConfigurationsPage />} />
        <Route path="/" element={<LoginPage />} /> {/* Default route */}
      </Routes>
    </Router>
  );
}

export default App;