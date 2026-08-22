import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Briefcase,
  FileCheck2,
  FileText,
  Bot,
  UserCheck,
  Building2,
  PlusCircle,
  Users,
  Settings,
  Sparkles,
} from 'lucide-react';

const Sidebar = () => {
  const { user, isStudent, isRecruiter } = useAuth();

  const studentLinks = [
    { to: '/student/dashboard', icon: LayoutDashboard, label: 'Overview' },
    { to: '/student/drives', icon: Briefcase, label: 'Explore Drives' },
    { to: '/student/applications', icon: FileCheck2, label: 'My Applications' },
    { to: '/student/resume', icon: FileText, label: 'Resume Studio' },
    { to: '/student/chat', icon: Bot, label: 'AI Career Agent' },
    { to: '/student/profile', icon: UserCheck, label: 'Profile & Skills' },
  ];

  const recruiterLinks = [
    { to: '/recruiter/dashboard', icon: LayoutDashboard, label: 'Recruiter Hub' },
    { to: '/recruiter/manage-drives', icon: Briefcase, label: 'Manage Drives' },
    { to: '/recruiter/post-drive', icon: PlusCircle, label: 'Post New Drive' },
    { to: '/recruiter/profile', icon: Building2, label: 'Company Profile' },
  ];

  const links = isStudent ? studentLinks : isRecruiter ? recruiterLinks : [];

  return (
    <aside className="w-64 bg-white border-r border-slate-200 min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between hidden lg:flex">
      <div className="space-y-6">
        {/* User Card */}
        <div className="p-3 bg-gradient-to-br from-brand-50 to-indigo-50/50 rounded-xl border border-brand-100 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-brand-600 text-white font-bold flex items-center justify-center text-sm shadow-sm">
            {isStudent
              ? user?.full_name?.charAt(0) || 'S'
              : user?.name?.charAt(0) || 'R'}
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-bold text-slate-900 truncate">
              {isStudent ? user?.full_name : user?.name}
            </p>
            <p className="text-xs text-brand-600 font-semibold truncate">
              {isStudent ? (user?.profile?.programme || 'Student') : (user?.industry || 'Recruiter')}
            </p>
          </div>
        </div>

        {/* Navigation List */}
        <div>
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2">
            Main Menu
          </p>
          <nav className="space-y-1">
            {links.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink
                  key={link.to}
                  to={link.to}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-brand-600 text-white shadow-sm shadow-brand-500/20 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{link.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Footer Feature Tip */}
      <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
        <div className="flex items-center gap-2 text-indigo-600 font-semibold text-xs mb-1">
          <Sparkles className="w-3.5 h-3.5" />
          <span>GraphRAG Intelligence</span>
        </div>
        <p className="text-[11px] text-slate-500 leading-relaxed">
          Evaluations strictly execute via deterministic policy nodes and Neo4j placement knowledge graphs.
        </p>
      </div>
    </aside>
  );
};

export default Sidebar;
