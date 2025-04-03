// src/components/CreateTemplate.jsx
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
    faCloudUploadAlt,
    faNetworkWired,
    faEnvelope,
    faPlus,
    faSearch,
} from '@fortawesome/free-solid-svg-icons';
import { faMicrosoft } from '@fortawesome/free-brands-svg-icons';
import Header from './Header';
import Sidebar from './SideMenu';
import Footer from './Footer';
import './CreateTemplate.css'; // Import the CSS file IMPORTANT

const API_BASE_URL = 'http://localhost:8000';

function CreateTemplate() {
    const [templates, setTemplates] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [templateName, setTemplateName] = useState('');
    const [templateData, setTemplateData] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);  // For file upload

    useEffect(() => {
        fetchTemplates(); // Fetch templates on component mount
    }, []); // Empty dependency array to run only once on mount

    const fetchTemplates = async () => {
        setIsLoading(true);
        setError(null);
        const token = localStorage.getItem('accessToken');

        if (!token) {
            setError(new Error('No access token found. Please log in.'));
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/templates`, {
                headers: {
                    'accept': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setTemplates(data);
        } catch (err) {
            setError(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);

        const token = localStorage.getItem('accessToken');

        if (!token) {
            setError(new Error('No access token found. Please log in.'));
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/templates/text?template_name=${templateName}`, {
                method: 'POST',
                headers: {
                    'accept': 'text/plain',
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'text/plain',
                },
                body: templateData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            fetchTemplates();
            setTemplateName('');
            setTemplateData('');
            setSelectedFile(null); // Clear selected file after successful submission

            alert('Template created successfully!');

        } catch (err) {
            setError(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileSelect = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);

        const reader = new FileReader();
        reader.onload = (e) => {
            setTemplateData(e.target.result); // Set textarea content to file content
        };
        reader.readAsText(file);
    };

    const handleDrop = (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        setSelectedFile(file);

        const reader = new FileReader();
        reader.onload = (e) => {
            setTemplateData(e.target.result); // Set textarea content to file content
        };
        reader.readAsText(file);
    };

    const handleDragOver = (event) => {
        event.preventDefault();
    };

    if (isLoading) {
        return <div className="text-center">Loading...</div>;
    }

    if (error) {
        return <div className="text-red-500 text-center">Error: {error.message}</div>;
    }

    return (
        <div className="create-template-container">
            {/* Page Header */}
            <Header />
            <div className="create-template-wrapper">

                <Sidebar />
                <main className="create-template-main">
                    <div className="create-template-header">
                        <h1 className="create-template-title">Templates</h1>
                    </div>

                    {/* Create Template Form */}
                    <div className="create-template-form-container">
                        <h2 className="create-template-form-title">Create New Template</h2>
                        <form className="create-template-form" onSubmit={handleSubmit}>
                            {/* Template Name */}
                            <div className="create-template-form-group">
                                <label className="create-template-label">Template Name</label>
                                <input
                                    type="text"
                                    className="create-template-input"
                                    placeholder="Enter template name"
                                    value={templateName}
                                    onChange={(e) => setTemplateName(e.target.value)}
                                    required
                                />
                            </div>

                            {/* Template Data */}
                            <div className="create-template-form-group">
                                <label className="create-template-label">Template Data</label>
                                <div
                                    className="create-template-file-upload-container"
                                    onDrop={handleDrop}
                                    onDragOver={handleDragOver}
                                >
                                    <textarea
                                        className="create-template-textarea"
                                        placeholder="Enter your template data here..."
                                        value={templateData}
                                        onChange={(e) => setTemplateData(e.target.value)}
                                        required
                                    />
                                    <div className="create-template-file-upload-overlay">
                                        <div className="create-template-file-upload-text">
                                            <FontAwesomeIcon icon={faCloudUploadAlt} className="create-template-file-upload-icon" />
                                            <p>Drag and drop your file here or click to browse</p>
                                            <input
                                                type="file"
                                                style={{ display: 'none' }}
                                                id="file-input"
                                                onChange={handleFileSelect}
                                            />
                                            <label htmlFor="file-input">Click to browse</label>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Submit Button */}
                            <div className="create-template-submit-container">
                                <button type="submit" className="create-template-submit-button">
                                    Create Template
                                </button>
                            </div>
                        </form>
                    </div>

                    {/* Latest Templates List */}
                    <div className="create-template-list-container">
                        <div className="create-template-list-header">
                            <h2 className="create-template-list-title">Latest Templates</h2>
                        </div>
                        <div className="create-template-list-table-container">
                            <table className="create-template-list-table">
                                <thead className="create-template-list-thead">
                                    <tr>
                                        <th className="create-template-list-th">Template Name</th>
                                        <th className="create-template-list-th">Created By</th>
                                        <th className="create-template-list-th">Created Date</th>
                                        <th className="create-template-list-th create-template-list-th-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="create-template-list-tbody">
                                    {templates.map(template => (
                                        <tr key={template._id}>
                                            <td className="create-template-list-td">{template.template_name}</td>
                                            <td className="create-template-list-td">{template.username}</td>
                                            <td className="create-template-list-td">{new Date(template.timestamp).toLocaleDateString()}</td>
                                            <td className="create-template-list-td create-template-list-td-right">Active</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </main>
            </div>
            <Footer />
        </div>
    );
}

export default CreateTemplate;
