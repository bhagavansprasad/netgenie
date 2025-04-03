import React, { useState, useEffect } from 'react';
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
import { Link, useNavigate } from 'react-router-dom';
import './dashboard.css'; // Import the CSS (Tailwind will process it)

function Dashboard() {
    const navigate = useNavigate();
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const API_BASE_URL = 'http://localhost:8000'; // Centralize the base URL

    useEffect(() => {
        const fetchMetrics = async () => {
            setIsLoading(true);
            setError(null);
            const token = localStorage.getItem('accessToken');

            if (!token) {
                setError(new Error('No access token found. Please log in.'));
                setIsLoading(false);
                return;
            }

            const headers = {
                'accept': 'application/json',
                'Authorization': `Bearer ${token}`,
            };

            try {
                const [templates, configValues, devices, customers, users] = await Promise.all([
                    fetch(`${API_BASE_URL}/templates`, { headers }).then(res => res.json()).then(data => data.length),
                    fetch(`${API_BASE_URL}/config_values/`, { headers }).then(res => res.json()).then(data => data.length),
                    fetch(`${API_BASE_URL}/devices/`, { headers }).then(res => res.json()).then(data => data.length),
                    fetch(`${API_BASE_URL}/customers/`, { headers }).then(res => res.json()).then(data => data.length),
                    fetch(`${API_BASE_URL}/list_users`, { headers }).then(res => res.json()).then(data => data.length),
                ]);

                const mockData = {
                    title: 'Dashboard Overview',
                    metrics: [
                        { name: 'Templates', value: templates, icon: faCode },
                        { name: 'Config Values', value: configValues, icon: faDatabase },
                        { name: 'Devices', value: devices, icon: faServer },
                        { name: 'Customers', value: customers, icon: faUsers },
                        { name: 'Users', value: users, icon: faUser },
                    ],
                    recentActivity: [
                        { text: 'Router Template Updated', icon: faCodeBranch, time: '2 hours ago' },
                        { text: 'New Device Added', icon: faServer, time: '5 hours ago' },
                        { text: 'Config Generated', icon: faCode, time: 'Yesterday' },
                    ],
                };
                setData(mockData);
            } catch (err) {
                setError(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchMetrics();
    }, []);  // Run only once on component mount


    const handleCreateTemplateClick = () => {
        navigate('/create-template');
    };
    const handleConfigurationValues = () => {
        navigate('/configurations');
    };
    const handleCreateNewDevice = () => {
        navigate('/new-device');
    };
    const handleCreateNewCustomer = () => {
        navigate('/new-customer');
    };
    const handleGenerateConfigurations = () => {
        navigate('/generate-configurations');
    };

    if (isLoading) {
        return <div className="text-center p-4">Loading dashboard data...</div>;
    }

    if (error) {
        return <div className="text-red-500 text-center p-4">Error: {error.message}</div>;
    }

    return (
        <>
            {/* Top Navigation Header */}
            <header className="bg-white border-b border-neutral-200 sticky top-0 z-50 shadow-sm">
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
                                <button
                                    className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100"
                                    onClick={handleCreateTemplateClick}
                                >
                                    <FontAwesomeIcon icon={faPlus} />
                                    Create Template
                                </button>
                                <button
                                    className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100"
                                    onClick={handleConfigurationValues}
                                >
                                    <FontAwesomeIcon icon={faCode} />
                                    Create Config Values
                                </button>
                                <button
                                    className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100"
                                    onClick={handleCreateNewDevice}
                                >
                                    <FontAwesomeIcon icon={faServer} />
                                    Create Device
                                </button>
                                <button
                                    className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100"
                                    onClick={handleCreateNewCustomer}
                                >
                                    <FontAwesomeIcon icon={faUsers} />
                                    Create Customer
                                </button>
                                <button
                                    className="flex items-center gap-2 px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-md hover:bg-neutral-100"
                                    onClick={handleGenerateConfigurations}
                                >
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
                                        {/* More template rows here... */}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* System Status */}
                        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
                            {data && data.metrics.map((metric) => (
                                <div key={metric.name} className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                                    <div className="flex items-center gap-4">
                                        <div className="w-16 h-16 rounded-full border-4 border-neutral-100 flex items-center justify-center bg-neutral-50">
                                            <FontAwesomeIcon icon={metric.icon} className="text-neutral-600 text-xl" />
                                        </div>
                                        <div>
                                            <p className="text-2xl text-neutral-800">{metric.value}</p>
                                            <p className="text-neutral-600">{metric.name}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Recent Activity */}
                        <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm backdrop-blur-sm">
                            <h2 className="text-lg mb-4">Recent Activity</h2>
                            <div className="space-y-4">
                                {data && data.recentActivity.map((activity, index) => (
                                    <div className="flex items-start gap-3" key={index}>
                                        <FontAwesomeIcon icon={activity.icon} className="mt-1 text-neutral-400" />
                                        <div>
                                            <p className="text-sm text-neutral-900">{activity.text}</p>
                                            <p className="text-xs text-neutral-500">{activity.time}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </>
    );
}

export default Dashboard;
