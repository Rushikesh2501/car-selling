import React from 'react';

interface NavbarProps {
  isChatOpen: boolean;
  onToggleChat: () => void;
  suggestedCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({ }) => {
  return (
    <nav className="navbar">
      <div className="brand" onClick={() => window.location.reload()}>
        <div className="brand-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9C2 11.1 2 11.3 2 11.5V16c0 .6.4 1 1 1h2" />
            <circle cx="7" cy="17" r="2" />
            <path d="M9 17h6" />
            <circle cx="17" cy="17" r="2" />
          </svg>
        </div>
        <span>Dream cars</span>
      </div>
    </nav>
  );
};
