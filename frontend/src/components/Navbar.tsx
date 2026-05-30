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
        <div className="brand-icon">A</div>
        <span>Dream cars</span>
      </div>
    </nav>
  );
};
