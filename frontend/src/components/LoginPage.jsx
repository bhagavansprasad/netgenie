// src/components/LoginPage.jsx
import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faNetworkWired,
  faEnvelope,
} from '@fortawesome/free-solid-svg-icons';
import { faMicrosoft } from '@fortawesome/free-brands-svg-icons';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'; // Import the CSS file
import { SERVER_URL } from '../../config';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append('grant_type', 'password');
      formData.append('username', email); // Use email as username
      formData.append('password', password);
      formData.append('scope', '');
      formData.append('client_id', 'string');
      formData.append('client_secret', 'string');

      const response = await fetch(`${SERVER_URL}/auth/login`, { // Use SERVER_URL from config
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (!response.ok) {
        // Handle login error (e.g., invalid credentials)
        console.error('Login failed:', response.status);
        alert('Login failed. Please check your credentials.'); // Consider a better error display
        return;
      }

      const data = await response.json();
      console.log(data);
      // Save the access token
      localStorage.setItem('accessToken', data.access_token);

      // Redirect to dashboard
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      alert('An error occurred during login.'); // Improve error display
    }
  };

  // Function to get the token for requests (place outside component if it doesn't use state)
  const getToken = () => {
    return localStorage.getItem('accessToken');
  };

  // Example usage of getToken (for demonstration)
  const makeAuthenticatedRequest = async () => {
    const token = getToken();
    if (token) {
      try {
        const response = await fetch('/some-api-endpoint', { // Replace with your endpoint
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json', // Example content type
          },
        });
        const data = await response.json();
        console.log('Authenticated data:', data);
      } catch (error) {
        console.error('Error making authenticated request:', error);
      }
    } else {
      console.warn('No token available. User is not logged in.');
    }
  };

  return (
<div className="login-container">
      <div className="login-wrapper">
        {/* Logo Section */}
        <div className="login-logo-section">
          <div className="login-logo-container">
            <FontAwesomeIcon icon={faNetworkWired} className="login-logo" />
            NetGenie
          </div>
          <p className="login-tagline">Network Configuration Management</p>
        </div>

        {/* Login Form */}
        <div className="login-form-container">
          <div className="login-form-content">
            {/* Login Options */}
            <div className="login-options">
              <button className="login-option-button">
                <FontAwesomeIcon icon={faEnvelope} />
                Email
              </button>
              <button className="login-option-button">
                <FontAwesomeIcon icon={faMicrosoft} />
                SSO
              </button>
            </div>

            <div className="login-separator-container">
              <div className="login-separator-line"></div>
              <div className="login-separator-text">
                or continue with email
              </div>
            </div>

            {/* Email Input */}
            <div className="login-input-group">
              <label className="login-label">Email</label>
              <input
                type="email"
                className="login-input"
                placeholder="name@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            {/* Password Input */}
            <div className="login-input-group">
              <label className="login-label">Password</label>
              <input
                type="password"
                className="login-input"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {/* Remember & Forgot */}
            <div className="login-remember-forgot">
              <div className="login-remember">
                <input
                  type="checkbox"
                  className="login-checkbox"
                />
                <label className="login-remember-label">Remember me</label>
              </div>
              <button className="login-forgot-button">
                Forgot password?
              </button>
            </div>

            {/* Login Button */}
            <button className="login-button" onClick={handleLogin}>
              Sign in
            </button>
          </div>
        </div>

        {/* Admin Registration */}
        <div className="login-admin-registration">
          <span className="login-admin-text">Need an account? </span>
          <button className="login-admin-button">Contact Admin</button>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;