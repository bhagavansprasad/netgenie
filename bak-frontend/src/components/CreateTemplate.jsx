// CreateTemplate.jsx (or similar name)
import React from 'react';
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

function CreateTemplate() {
    return (
        <div className="flex-1 p-6">
            {/* Page Header */}
            <Header />
            <div className="flex min-h-screen bg-[#f5f5f5]">

                <Sidebar />
                <main className="flex-1 p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-2xl text-neutral-800">Templates</h1>
                        {/*The below Create template button is not required here, as we are already in the create template page*/}
                        {/*                <button className="flex items-center gap-2 px-4 py-2 bg-neutral-800 text-white rounded-md hover:bg-neutral-900">
                            <FontAwesomeIcon icon={faPlus} />
                            Create Template
                        </button>*/}
                    </div>

                    {/* Create Template Form */}
                    <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm mb-6">
                        <h2 className="text-lg mb-6">Create New Template</h2>
                        <form className="space-y-6">
                            {/* Template Name */}
                            <div>
                                <label className="block text-sm text-neutral-700 mb-1">Template Name</label>
                                <input type="text" className="w-full px-3 py-2 bg-white border border-neutral-200 rounded-md" placeholder="Enter template name" />
                            </div>

                            {/* Template Data */}
                            <div>
                                <label className="block text-sm text-neutral-700 mb-1">Template Data</label>
                                <div className="relative">
                                    <textarea className="w-full h-64 px-3 py-2 bg-white border border-neutral-200 rounded-md" placeholder="Enter your template data here..."></textarea>
                                    <div className="absolute inset-0 flex items-center justify-center border-2 border-dashed border-neutral-300 rounded-md bg-neutral-50 opacity-0 hover:opacity-100 transition-opacity">
                                        <div className="text-center">
                                            <FontAwesomeIcon icon={faCloudUploadAlt} className="text-3xl text-neutral-400 mb-2" />
                                            <p className="text-neutral-600">Drag and drop your file here or click to browse</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Submit Button */}
                            <div className="flex justify-end">
                                <button type="submit" className="px-6 py-2 bg-neutral-800 text-white rounded-md hover:bg-neutral-900">
                                    Create Template
                                </button>
                            </div>
                        </form>
                    </div>

                    {/* Latest Templates List */}
                    <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-lg">Latest Templates</h2>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-neutral-50 border-b border-neutral-200">
                                    <tr>
                                        <th className="text-left p-4 text-sm text-neutral-600">Template Name</th>
                                        <th className="text-left p-4 text-sm text-neutral-600">Created By</th>
                                        <th className="text-left p-4 text-sm text-neutral-600">Created Date</th>
                                        <th className="text-right p-4 text-sm text-neutral-600">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-neutral-200">
                                    {/* Template rows will be dynamically populated */}
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