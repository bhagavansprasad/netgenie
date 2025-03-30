// Header.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
    faNetworkWired,
    faBell,
    faSearch,
} from '@fortawesome/free-solid-svg-icons';

function Header() {
    return (
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
    );
}

export default Header;