import { ReactNode } from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, GraduationCap, FileText, Calendar, BookOpen } from 'lucide-react';

import './AppShell.css';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/evaluations', label: 'Evaluations', icon: GraduationCap },
  { to: '/essays', label: 'Essays', icon: FileText },
  { to: '/planner', label: 'Planner', icon: Calendar }
];

export const AppShell = ({ children }: { children: ReactNode }) => {
  return (
    <div className="app-shell">
      <aside className="app-shell__sidebar">
        <div className="app-shell__header">
          <BookOpen className="app-shell__logo-icon" size={32} />
          <h1 className="app-shell__logo">Counselor</h1>
        </div>
        <nav>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `app-shell__nav-item ${isActive ? 'app-shell__nav-item--active' : ''}`
              }
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="app-shell__content">{children}</main>
    </div>
  );
};
