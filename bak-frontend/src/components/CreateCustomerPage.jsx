// CreateCustomerPage.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Header from './Header';
import Sidebar from './SideMenu';
import Footer from './Footer';

function CreateCustomerPage() {
    return (
        <div className="flex-1 p-6">
            <Header />
            <div className="flex min-h-screen bg-[#f5f5f5]">
                <Sidebar />
                <main className="flex-1 p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-2xl text-neutral-800">Create Customer</h1>
                    </div>

                    {/* Create Customer Form */}
                    <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm mb-6">
                        <form className="space-y-6">
                            {/* Customer Name */}
                            <div>
                                <label className="block text-sm text-neutral-700 mb-1">Name</label>
                                <input type="text" className="w-full px-3 py-2 bg-white border border-neutral-200 rounded-md" placeholder="Enter customer name" />
                            </div>

                            {/* Submit Button */}
                            <div className="flex justify-end">
                                <button type="submit" className="px-6 py-2 bg-neutral-800 text-white rounded-md hover:bg-neutral-900">
                                    Create Customer
                                </button>
                            </div>
                        </form>
                    </div>

                    {/* Latest Customers List */}
                    <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-lg">Latest Customers</h2>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-neutral-50 border-b border-neutral-200">
                                    <tr>
                                        <th className="text-left p-4 text-sm text-neutral-600">Name</th>
                                        <th className="text-right p-4 text-sm text-neutral-600">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-neutral-200">
                                    {/* Customer rows will be dynamically populated */}
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

export default CreateCustomerPage;