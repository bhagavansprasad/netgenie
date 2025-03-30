// GenerateConfigurationsPage.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Header from './Header';
import Sidebar from './SideMenu';
import Footer from './Footer';

function GenerateConfigurationsPage() {
    return (
        <div className="flex-1 p-6">
            <Header />
            <div className="flex min-h-screen bg-[#f5f5f5]">
                <Sidebar />
                <main className="flex-1 p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-2xl text-neutral-800">Generate Configuration</h1>
                    </div>

                    {/* Generate Configuration Form */}
                    <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm mb-6">
                        <form className="space-y-6">
                            {/* Device Name Dropdown */}
                            <div>
                                <label className="block text-sm text-neutral-700 mb-1">Device Name</label>
                                <select className="w-full px-3 py-2 bg-white border border-neutral-200 rounded-md">
                                    <option value="">Select Device</option>
                                    <option value="device1">Device 1</option>
                                    <option value="device2">Device 2</option>
                                </select>
                            </div>

                            {/* Template Name Dropdown */}
                            <div>
                                <label className="block text-sm text-neutral-700 mb-1">Template Name</label>
                                <select className="w-full px-3 py-2 bg-white border border-neutral-200 rounded-md">
                                    <option value="">Select Template</option>
                                    <option value="template1">Template 1</option>
                                    <option value="template2">Template 2</option>
                                </select>
                            </div>

                            {/* Config Values Dropdown */}
                            <div>
                                <label className="block text-sm text-neutral-700 mb-1">Config Values</label>
                                <select className="w-full px-3 py-2 bg-white border border-neutral-200 rounded-md">
                                    <option value="">Select Config Values</option>
                                    <option value="config1">Config Values 1</option>
                                    <option value="config2">Config Values 2</option>
                                </select>
                            </div>

                            {/* Generate Button */}
                            <div className="flex justify-end">
                                <button type="submit" className="px-6 py-2 bg-neutral-800 text-white rounded-md hover:bg-neutral-900">
                                    Generate Configuration
                                </button>
                            </div>
                        </form>
                    </div>

                    {/* Generated Configurations List */}
                    <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-lg">Recent Configurations</h2>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-neutral-50 border-b border-neutral-200">
                                    <tr>
                                        <th className="text-left p-4 text-sm text-neutral-600">Device</th>
                                        <th className="text-left p-4 text-sm text-neutral-600">Template</th>
                                        <th className="text-left p-4 text-sm text-neutral-600">Config Values</th>
                                        <th className="text-right p-4 text-sm text-neutral-600">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-neutral-200">
                                    {/* Configuration rows will be dynamically populated */}
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

export default GenerateConfigurationsPage;