import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { healthApi } from '../api/services';
import {
  Sparkles,
  User,
  Building2,
  LogOut,
  Menu,
  X,
  Activity,
  Briefcase,
  Layers,
  Bot,
  FileText,
  FileCheck,
} from 'lucide-react';

const Navbar = () => {
  const { user, isAuthenticated, isStudent, isRecruiter, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const checkServer = async () => {
      try {
        await healthApi.checkHealth();
        setBackendStatus('online');
      } catch (err) {
        setBackendStatus('offline');
      }
    };
    checkServer();
    const interval = setInterval(checkServer, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200 shadow-sm transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5 text-indigo-100" />
            </div>
            <div>
              <span className="text-xl font-bold bg-gradient-to-r from-brand-700 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
                CareerConnect
              </span>
              <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 ml-1.5 px-1.5 py-0.5 bg-brand-50 rounded">
                AI
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-1">
            {isAuthenticated ? (
              <>
                {isStudent && (
                  <>
                    <Link
                      to="/student/dashboard"
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive('/student/dashboard')
                          ? 'bg-brand-50 text-brand-700 font-semibold'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }`}
                    >
                      Dashboard
                    </Link>
                    <Link
                      to="/student/drives"
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive('/student/drives')
                          ? 'bg-brand-50 text-brand-700 font-semibold'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }`}
                    >
                      Explore Drives
                    </Link>
                    <Link
                      to="/student/applications"
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive('/student/applications')
                          ? 'bg-brand-50 text-brand-700 font-semibold'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }`}
                    >
                      My Applications
                    </Link>
                    <Link
                      to="/student/resume"
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive('/student/resume')
                          ? 'bg-brand-50 text-brand-700 font-semibold'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }`}
                    >
                      Resume Studio
                    </Link>
                    <Link
                      to="/student/chat"
                      className={`px-3 py-2 rounded-lg text-sm font-medium flex items-center gap-1.5 transition-colors ${
                        isActive('/student/chat')
                          ? 'bg-purple-50 text-purple-700 font-semibold'
                          : 'text-purple-600 hover:bg-purple-50'
                      }`}
                    >
                      <Bot className="w-4 h-4" />
                      AI Assistant
                    </Link>
                  </>
                )}

                {isRecruiter && (
                  <>
                    <Link
                      to="/recruiter/dashboard"
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive('/recruiter/dashboard')
                          ? 'bg-brand-50 text-brand-700 font-semibold'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }`}
                    >
                      Recruiter Hub
                    </Link>
                    <Link
                      to="/recruiter/manage-drives"
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive('/recruiter/manage-drives')
                          ? 'bg-brand-50 text-brand-700 font-semibold'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                      }`}
                    >
                      Manage Drives
                    </Link>
                    <Link
                      to="/recruiter/post-drive"
                      className={`px-3 py-2 rounded-lg text-sm font-medium bg-brand-600 text-white hover:bg-brand-700 shadow-sm transition-all`}
                    >
                      + Post New Drive
                    </Link>
                  </>
                )}
              </>
            ) : (
              <>
                <Link
                  to="/"
                  className="px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                >
                  Overview
                </Link>
                <Link
                  to="/student/drives"
                  className="px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                >
                  Live Drives
                </Link>
              </>
            )}
          </nav>

          {/* Right Action Menu: Status, User Badge, Sign In/Out */}
          <div className="hidden md:flex items-center gap-3">
            {/* Backend status indicator */}
            <div
              className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600"
              title={`FastAPI Backend: ${backendStatus}`}
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  backendStatus === 'online'
                    ? 'bg-emerald-500 animate-pulse'
                    : backendStatus === 'checking'
                    ? 'bg-amber-400'
                    : 'bg-rose-500'
                }`}
              />
              <span className="capitalize">{backendStatus === 'online' ? 'API Connected' : backendStatus}</span>
            </div>

            {isAuthenticated ? (
              <div className="flex items-center gap-2">
                <Link
                  to={isStudent ? '/student/profile' : '/recruiter/profile'}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors"
                >
                  <div className="w-7 h-7 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center font-bold text-xs">
                    {isStudent
                      ? user?.full_name?.charAt(0) || 'S'
                      : user?.name?.charAt(0) || 'R'}
                  </div>
                  <div className="text-left">
                    <p className="text-xs font-semibold text-slate-800 leading-tight">
                      {isStudent ? user?.full_name : user?.name}
                    </p>
                    <p className="text-[10px] text-slate-500 uppercase tracking-wider font-bold">
                      {user?.role}
                    </p>
                  </div>
                </Link>

                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                  title="Sign Out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/auth"
                  className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-brand-600 hover:bg-slate-50 rounded-lg transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/auth?mode=register"
                  className="px-4 py-2 text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-lg shadow-sm shadow-brand-500/20 transition-all"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center gap-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-600 hover:text-slate-900 rounded-lg"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-200 bg-white px-4 pt-2 pb-6 space-y-2 shadow-lg">
          {isAuthenticated ? (
            <>
              <div className="py-2 border-b border-slate-100 mb-2">
                <p className="text-sm font-bold text-slate-800">
                  {isStudent ? user?.full_name : user?.name}
                </p>
                <p className="text-xs text-slate-500">{user?.email} ({user?.role})</p>
              </div>
              {isStudent && (
                <>
                  <Link
                    to="/student/dashboard"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-md"
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/student/drives"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-md"
                  >
                    Explore Drives
                  </Link>
                  <Link
                    to="/student/applications"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-md"
                  >
                    My Applications
                  </Link>
                  <Link
                    to="/student/resume"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-md"
                  >
                    Resume Studio
                  </Link>
                  <Link
                    to="/student/chat"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-purple-700 hover:bg-purple-50 rounded-md"
                  >
                    AI Assistant
                  </Link>
                  <Link
                    to="/student/profile"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-md"
                  >
                    My Profile
                  </Link>
                </>
              )}
              {isRecruiter && (
                <>
                  <Link
                    to="/recruiter/dashboard"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-md"
                  >
                    Recruiter Hub
                  </Link>
                  <Link
                    to="/recruiter/manage-drives"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-md"
                  >
                    Manage Drives
                  </Link>
                  <Link
                    to="/recruiter/post-drive"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-brand-600 font-semibold"
                  >
                    + Post New Drive
                  </Link>
                  <Link
                    to="/recruiter/profile"
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-md"
                  >
                    Company Profile
                  </Link>
                </>
              )}
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  handleLogout();
                }}
                className="w-full text-left px-3 py-2 text-sm font-medium text-rose-600 hover:bg-rose-50 rounded-md"
              >
                Sign Out
              </button>
            </>
          ) : (
            <div className="space-y-2 pt-2">
              <Link
                to="/auth"
                onClick={() => setMobileMenuOpen(false)}
                className="block text-center py-2 text-sm font-semibold text-brand-600 bg-brand-50 rounded-lg"
              >
                Sign In
              </Link>
              <Link
                to="/auth?mode=register"
                onClick={() => setMobileMenuOpen(false)}
                className="block text-center py-2 text-sm font-semibold text-white bg-brand-600 rounded-lg"
              >
                Register Account
              </Link>
            </div>
          )}
        </div>
      )}
    </header>
  );
};

export default Navbar;
