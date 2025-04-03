// Footer.jsx
import React from 'react';

function Footer() {
    return (
        <footer className="bg-white border-t border-neutral-200 p-4 text-center text-neutral-600">
            <p>© {new Date().getFullYear()} NetGenie. All rights reserved.</p>
        </footer>
    );
}

export default Footer;