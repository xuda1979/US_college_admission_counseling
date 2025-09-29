import { ReactNode } from 'react';
import { NavLink } from 'react-router-dom';

import './AppShell.css';

const navItems = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/evaluations', label: 'Evaluations' },
  { to: '/essays', label: 'Essays' },
  { to: '/planner', label: 'Planner' }
];

export const AppShell = ({ children }: { children: ReactNode }) => {
  return (
    <div className="app-shell">
      <aside className="app-shell__sidebar">
        <h1 className="app-shell__logo">Counselor</h1>
        <nav>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `app-shell__nav-item ${isActive ? 'app-shell__nav-item--active' : ''}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="app-shell__content">{children}</main>
    </div>
  );
};
