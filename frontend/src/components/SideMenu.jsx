// Sidebar.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
    faHouse,
    faCode,
    faGear,
    faServer,
    faUsers,
    faUserShield,
    faChartLine,
    faCog,
} from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';

function Sidebar() {
    return (
        <aside className="w-64 bg-white border-r border-neutral-200 p-4">
            <nav className="space-y-1">
                <Link to="/dashboard" className="flex items-center gap-3 px-3 py-2 text-neutral-900 bg-neutral-100 rounded-md">
                    <FontAwesomeIcon icon={faHouse} />
                    <span>Dashboard</span>
                </Link>
                <Link to="/network-templates" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                    <FontAwesomeIcon icon={faCode} />
                    <span>Network Templates</span>
                </Link>
                <Link to="/configuration" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                    <FontAwesomeIcon icon={faGear} />
                    <span>Configuration</span>
                </Link>
                <Link to="/devices" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                    <FontAwesomeIcon icon={faServer} />
                    <span>Devices</span>
                </Link>
                <Link to="/customers" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                    <FontAwesomeIcon icon={faUsers} />
                    <span>Customers</span>
                </Link>
                <Link to="/users-roles" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                    <FontAwesomeIcon icon={faUserShield} />
                    <span>Users & Roles</span>
                </Link>
                <Link to="/reports-logs" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                    <FontAwesomeIcon icon={faChartLine} />
                    <span>Reports & Logs</span>
                </Link>
                <Link to="/settings" className="flex items-center gap-3 px-3 py-2 text-neutral-600 hover:bg-neutral-100 rounded-md">
                    <FontAwesomeIcon icon={faCog} />
                    <span>Settings</span>
                </Link>
            </nav>
        </aside>
    );
}

export default Sidebar;