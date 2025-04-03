import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
    faNetworkWired,
    faEnvelope,
    faBell,
    faSearch,
    faHouse,
    faCode,
    faGear,
    faServer,
    faUsers,
    faUserShield,
    faChartLine,
    faCog,
    faPlus,
    faCodeBranch,
    faDatabase,
    faUser,
} from '@fortawesome/free-solid-svg-icons';
import { faMicrosoft } from '@fortawesome/free-brands-svg-icons';
import { Link, useNavigate } from 'react-router-dom';

function Dashboard() {
    const navigate = useNavigate();

    const handleCreateTemplateClick = () => {
        navigate('/create-template'); // Programmatically navigate
    };
    const handleConfigurationValues = () => {
        navigate('/configurations'); // Programmatically navigate
    };
    const handleCreateNewDevice = () => {
        navigate('/new-device'); // Programmatically navigate
    };
    const handleCreateNewCustomer = () => {
        navigate('/new-customer'); // Programmatically navigate
    };
    const handleGenerateConfigurations = () => {
        navigate('/generate-configurations'); // Programmatically navigate
    };

    return (
        <>
            {/* Top Navigation Header */}
            <header id="header" className="bg-white border-b border-neutral-200 sticky top-0 z-50 shadow-sm">
                <div className="px-4 flex h-14 items-center justify-between">
                    {/* Logo */}
                    <div className="flex items-center gap-2">
                        <FontAwesomeIcon icon={faNetworkWired} className="text-2xl text-neutral-800" />
                        <span className="text-xl text-neutral-800">NetGenie</span>
                    </div>

                    {/* Search */}
                    <div className="hidden md:flex flex-1 max-w-xl mx-8">
                        <div className="relative w-full">
                            <input type="search" className="w-full pl-10 pr-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md" placeholder="Search..." />
                            <FontAwesomeIcon icon={faSearch} className="absolute left-3 top-3 text-neutral-400" />
                        </div>
                    </div>

                    {/* Right Actions */}
                    <div className="flex items-center gap-4">
                        <button className="relative">
                            <FontAwesomeIcon icon={faBell} className="text-xl text-neutral-600" />
                            <span className="absolute -top-1 -right-1 w-2 h-2 bg-neutral-800 rounded-full"></span>
                        </button>
                        <img src="https://api.dicebear.com/7.x/notionists/svg?scale=200&seed=123" alt="User" className="w-8 h-8 rounded-full" />
                    </div>
                </div>
            </header>

            {/* Main Layout */}
            <div className="flex min-h-screen bg-[#f5f5f5]">
                {/* Sidebar */}
                <aside className="w-64 bg-white border-r border-neutral-200 p-4 shadow-sm">
                    <nav className="space-y-1">
                        <a href="#" className="flex items-center gap-3 px-3 py-2 text-neutral-900 bg-neutral-100 rounded-md">
                            <FontAwesomeIcon icon={faHouse} />
                            <span>Dashboard</span>
                        </a>
                        <a href="#" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                            <FontAwesomeIcon icon={faCode} />
                            <span>Network Templates</span>
                        </a>
                        <a href="#" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                            <FontAwesomeIcon icon={faGear} />
                            <span>Configuration</span>
                        </a>
                        <a href="#" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                            <FontAwesomeIcon icon={faServer} />
                            <span>Devices</span>
                        </a>
                        <a href="#" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                            <FontAwesomeIcon icon={faUsers} />
                            <span>Customers</span>
                        </a>
                        <a href="#" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                            <FontAwesomeIcon icon={faUserShield} />
                            <span>Users & Roles</span>
                        </a>
                        <a href="#" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                            <FontAwesomeIcon icon={faChartLine} />
                            <span>Reports & Logs</span>
                        </a>
                        <a href="#" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                            <FontAwesomeIcon icon={faCog} />
                            <span>Settings</span>
                        </a>
                    </nav>
                </aside>

                {/* Main Content */}
                <main className="flex-1 p-6">
                    <div className="grid grid-cols-1 gap-6">
                        {/* Quick Actions */}
                        <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                            <h2 className="text-lg mb-4">Quick Actions</h2>
                            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                                {/* <Link to="/dashboard/create-template" // Use Link for navigation
                                      className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100">
                                       <FontAwesomeIcon icon={faPlus} />
                                       Create Template
                                </Link> */}
                                <button className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100" onClick={handleCreateTemplateClick}>
                                    <FontAwesomeIcon icon={faPlus} />
                                    Create Template
                                </button>
                                <button className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100" onClick={handleConfigurationValues}>
                                    <FontAwesomeIcon icon={faCode} />
                                    Create Config Values
                                </button>
                                <button className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100" onClick={handleCreateNewDevice}>
                                    <FontAwesomeIcon icon={faServer} />
                                    Create Device
                                </button>
                                <button className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100" onClick={handleCreateNewCustomer}>
                                    <FontAwesomeIcon icon={faUsers} />
                                    Create Customer
                                </button>
                                <button className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100" onClick={handleGenerateConfigurations}>
                                    <FontAwesomeIcon icon={faGear} />
                                    Generate Configuration
                                </button>
                            </div>
                        </div>

                        {/* Latest Templates */}
                        <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                            <h2 className="text-lg mb-4">Latest Templates</h2>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="border-b border-neutral-200">
                                            <th className="text-left py-3 px-4 text-sm text-neutral-600">Template Name</th>
                                            <th className="text-left py-3 px-4 text-sm text-neutral-600">Created By</th>
                                            <th className="text-left py-3 px-4 text-sm text-neutral-600">Created Date</th>
                                            <th className="text-left py-3 px-4 text-sm text-neutral-600">Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr className="border-b border-neutral-100">
                                            <td className="py-3 px-4 text-sm">Router Base Config</td>
                                            <td className="py-3 px-4 text-sm">John Doe</td>
                                            <td className="py-3 px-4 text-sm">Jan 15, 2025</td>
                                            <td className="py-3 px-4 text-sm"><span className="px-2 py-1 bg-neutral-100 rounded-full text-xs">Active</span></td>
                                        </tr>
                                        <tr className="border-b border-neutral-100">
                                            <td className="py-3 px-4 text-sm">Switch VLAN Template</td>
                                            <td className="py-3 px-4 text-sm">Jane Smith</td>
                                            <td className="py-3 px-4 text-sm">Jan 14, 2025</td>
                                            <td className="py-3 px-4 text-sm"><span className="px-2 py-1 bg-neutral-100 rounded-full text-xs">Active</span></td>
                                        </tr>
                                        <tr className="border-b border-neutral-100">
                                            <td className="py-3 px-4 text-sm">Firewall Rules</td>
                                            <td className="py-3 px-4 text-sm">Mike Johnson</td>
                                            <td className="py-3 px-4 text-sm">Jan 13, 2025</td>
                                            <td className="py-3 px-4 text-sm"><span className="px-2 py-1 bg-neutral-100 rounded-full text-xs">Active</span></td>
                                        </tr>
                                        <tr className="border-b border-neutral-100">
                                            <td className="py-3 px-4 text-sm">ACL Template</td>
                                            <td className="py-3 px-4 text-sm">Sarah Wilson</td>
                                            <td className="py-3 px-4 text-sm">Jan 12, 2025</td>
                                            <td className="py-3 px-4 text-sm"><span className="px-2 py-1 bg-neutral-100 rounded-full text-xs">Active</span></td>
                                        </tr>
                                        <tr>
                                            <td className="py-3 px-4 text-sm">QoS Configuration</td>
                                            <td className="py-3 px-4 text-sm">Tom Brown</td>
                                            <td className="py-3 px-4 text-sm">Jan 11, 2025</td>
                                            <td className="py-3 px-4 text-sm"><span className="px-2 py-1 bg-neutral-100 rounded-full text-xs">Active</span></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* System Status */}
                        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                                <div className="flex items-center gap-4">
                                    <div className="w-16 h-16 rounded-full border-4 border-neutral-100 flex items-center justify-center bg-neutral-50">
                                        <FontAwesomeIcon icon={faCode} className="text-neutral-600 text-xl" />
                                    </div>
                                    <div>
                                        <p className="text-2xl text-neutral-800">48</p>
                                        <p className="text-neutral-600">Templates</p>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                                <div className="flex items-center gap-4">
                                    <div className="w-16 h-16 rounded-full border-4 border-neutral-100 flex items-center justify-center bg-neutral-50">
                                        <FontAwesomeIcon icon={faDatabase} className="text-neutral-600 text-xl" />
                                    </div>
                                    <div>
                                        <p className="text-2xl text-neutral-800">892</p>
                                        <p className="text-neutral-600">Config Values</p>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                                <div className="flex items-center gap-4">
                                    <div className="w-16 h-16 rounded-full border-4 border-neutral-100 flex items-center justify-center bg-neutral-50">
                                        <FontAwesomeIcon icon={faServer} className="text-neutral-600 text-xl" />
                                    </div>
                                    <div>
                                        <p className="text-2xl text-neutral-800">156</p>
                                        <p className="text-neutral-600">Devices</p>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                                <div className="flex items-center gap-4">
                                    <div className="w-16 h-16 rounded-full border-4 border-neutral-100 flex items-center justify-center bg-neutral-50">
                                        <FontAwesomeIcon icon={faUsers} className="text-neutral-600 text-xl" />
                                    </div>
                                    <div>
                                        <p className="text-2xl text-neutral-800">125</p>
                                        <p className="text-neutral-600">Customers</p>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                                <div className="flex items-center gap-4">
                                    <div className="w-16 h-16 rounded-full border-4 border-neutral-100 flex items-center justify-center bg-neutral-50">
                                        <FontAwesomeIcon icon={faUser} className="text-neutral-600 text-xl" />
                                    </div>
                                    <div>
                                        <p className="text-2xl text-neutral-800">32</p>
                                        <p className="text-neutral-600">Users</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Recent Activity */}
                        <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                            <h2 className="text-lg mb-4">Recent Activity</h2>
                            <div className="space-y-4">
                                <div className="flex items-start gap-3">
                                    <FontAwesomeIcon icon={faCodeBranch} className="mt-1 text-neutral-400" />
                                    <div>
                                        <p className="text-sm text-neutral-900">Router Template Updated</p>
                                        <p className="text-xs text-neutral-500">2 hours ago</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <FontAwesomeIcon icon={faServer} className="mt-1 text-neutral-400" />
                                    <div>
                                        <p className="text-sm text-neutral-900">New Device Added</p>
                                        <p className="text-xs text-neutral-500">5 hours ago</p>
                                    </div>
                                </div>
                                <div className="flex items-start gap-3">
                                    <FontAwesomeIcon icon={faCode} className="mt-1 text-neutral-400" />
                                    <div>
                                        <p className="text-sm text-neutral-900">Config Generated</p>
                                        <p className="text-xs text-neutral-500">Yesterday</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </>
    );
}

export default Dashboard;