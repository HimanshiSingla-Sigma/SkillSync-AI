import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { applicationApi, driveApi, resumeApi } from '../../api/services';
import { StatusBadge } from '../../components/StatusBadge';
import {
  GraduationCap,
  Briefcase,
  FileText,
  Bot,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  FileCheck2,
  TrendingUp,
  Award,
  Layers,
} from 'lucide-react';

const StudentDashboard = () => {
  const { user } = useAuth();
  const [applications, setApplications] = useState([]);
  const [drives, setDrives] = useState([]);
  const [resumeData, setResumeData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [apps, liveDrives] = await Promise.all([
          applicationApi.getMyApplications().catch(() => []),
          driveApi.listDrives('PUBLISHED', 0, 5).catch(() => []),
        ]);
        setApplications(apps || []);
        setDrives(liveDrives || []);

        try {
          const res = await resumeApi.getMyResume();
          setResumeData(res);
        } catch {
          setResumeData(null);
        }
      } catch (err) {
        console.error('Error loading dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };
    loadDashboardData();
  }, []);

  const totalApps = applications.length;
  const shortlistedCount = applications.filter((a) =>
    ['SHORTLISTED', 'ASSESSMENT', 'INTERVIEW', 'SELECTED'].includes(a.status?.toUpperCase())
  ).length;
  const selectedCount = applications.filter((a) =>
    ['SELECTED'].includes(a.status?.toUpperCase())
  ).length;

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-brand-700 via-indigo-600 to-purple-600 rounded-3xl p-6 sm:p-8 text-white shadow-lg shadow-brand-500/15 relative overflow-hidden">
        <div className="absolute right-0 top-0 w-80 h-80 bg-white/10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none" />
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 backdrop-blur-md text-xs font-semibold uppercase tracking-wider mb-3">
            <Sparkles className="w-3.5 h-3.5 text-yellow-300" />
            Student Placement Portal
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome back, {user?.full_name}!
          </h1>
          <p className="text-indigo-100 text-sm sm:text-base mt-2">
            Track your recruitment drives, verified policy eligibility, automated resume analysis,
            and AI GraphRAG career recommendations.
          </p>

          <div className="flex flex-wrap gap-3 mt-5">
            <Link
              to="/student/drives"
              className="px-4 py-2 bg-white text-brand-700 hover:bg-indigo-50 font-bold text-xs rounded-xl shadow transition-all flex items-center gap-1.5"
            >
              <Briefcase className="w-4 h-4" />
              Explore Placement Drives
            </Link>
            <Link
              to="/student/chat"
              className="px-4 py-2 bg-purple-500/40 hover:bg-purple-500/60 border border-purple-300/30 text-white font-bold text-xs rounded-xl transition-all flex items-center gap-1.5"
            >
              <Bot className="w-4 h-4" />
              Ask AI Career Agent
            </Link>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Verified CGPA
            </span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
              <Award className="w-4 h-4" />
            </div>
          </div>
          <p className="text-2xl font-black text-slate-900 mt-2">
            {user?.profile?.cgpa ? user.profile.cgpa.toFixed(2) : 'N/A'}
          </p>
          <p className="text-xs text-slate-500 mt-1">
            Backlogs: <span className="font-semibold text-slate-700">{user?.profile?.backlogs ?? 0}</span>
          </p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Skill Graph Nodes
            </span>
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
              <Layers className="w-4 h-4" />
            </div>
          </div>
          <p className="text-2xl font-black text-slate-900 mt-2">
            {user?.skills?.length || 0}
          </p>
          <p className="text-xs text-slate-500 mt-1">
            Synced to Neo4j Graph
          </p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Applications
            </span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-xl">
              <FileCheck2 className="w-4 h-4" />
            </div>
          </div>
          <p className="text-2xl font-black text-slate-900 mt-2">{totalApps}</p>
          <p className="text-xs text-slate-500 mt-1">
            Shortlisted: <span className="font-semibold text-brand-600">{shortlistedCount}</span>
          </p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Resume Status
            </span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-xl">
              <FileText className="w-4 h-4" />
            </div>
          </div>
          <p className="text-base font-bold text-slate-900 mt-2 truncate">
            {resumeData ? 'Parsed & Synced' : 'Not Uploaded'}
          </p>
          <Link
            to="/student/resume"
            className="text-xs font-semibold text-brand-600 hover:text-brand-700 mt-1 inline-block"
          >
            {resumeData ? 'Manage Resume →' : 'Upload Resume →'}
          </Link>
        </div>
      </div>

      {/* Grid: Live Placement Drives & Active Applications */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Live Drives Column */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <div className="flex justify-between items-center mb-5">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Open Placement Drives</h2>
              <p className="text-xs text-slate-500">
                Check eligibility policies and submit applications
              </p>
            </div>
            <Link
              to="/student/drives"
              className="text-xs font-bold text-brand-600 hover:text-brand-700 flex items-center gap-1"
            >
              View All <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {loading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-20 bg-slate-100 rounded-xl animate-pulse" />
              ))}
            </div>
          ) : drives.length === 0 ? (
            <p className="text-sm text-slate-500 py-6 text-center">No active drives published yet.</p>
          ) : (
            <div className="space-y-3">
              {drives.slice(0, 4).map((drive) => (
                <div
                  key={drive.id}
                  className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 hover:bg-slate-50 hover:border-slate-200 transition-all flex items-center justify-between"
                >
                  <div>
                    <span className="text-[11px] font-bold uppercase tracking-wider text-brand-600">
                      {drive.company_name}
                    </span>
                    <h3 className="text-sm font-bold text-slate-900 mt-0.5">{drive.title}</h3>
                    <div className="flex items-center gap-3 text-xs text-slate-500 mt-1">
                      <span>Package: <strong className="text-slate-800">{drive.salary_package}</strong></span>
                      <span>•</span>
                      <span>Min CGPA: <strong>{drive.eligibility_criteria?.min_cgpa || 0}</strong></span>
                    </div>
                  </div>
                  <Link
                    to="/student/drives"
                    className="px-3 py-1.5 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-lg shadow-sm"
                  >
                    Check & Apply
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Profile Summary / Applications Tracker Column */}
        <div className="space-y-6">
          {/* Applications Widget */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-base font-bold text-slate-900">Recent Applications</h2>
              <Link to="/student/applications" className="text-xs font-bold text-brand-600">
                View All
              </Link>
            </div>

            {applications.length === 0 ? (
              <div className="text-center py-6">
                <FileCheck2 className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                <p className="text-xs text-slate-500">You haven't applied to any drives yet.</p>
                <Link
                  to="/student/drives"
                  className="mt-2 inline-block text-xs font-bold text-brand-600 hover:underline"
                >
                  Explore open drives →
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {applications.slice(0, 3).map((app) => (
                  <div
                    key={app.id}
                    className="p-3 rounded-xl border border-slate-100 bg-slate-50 flex items-center justify-between"
                  >
                    <div className="overflow-hidden mr-2">
                      <p className="text-xs font-bold text-slate-900 truncate">
                        {app.drive_title}
                      </p>
                      <p className="text-[11px] text-slate-500 truncate">{app.company_name}</p>
                    </div>
                    <StatusBadge status={app.status} />
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Skills Node Card */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <div className="flex justify-between items-center mb-3">
              <h2 className="text-base font-bold text-slate-900">Your Skills</h2>
              <Link to="/student/profile" className="text-xs font-bold text-brand-600">
                Edit
              </Link>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {user?.skills?.length ? (
                user.skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-1 bg-brand-50 text-brand-700 rounded-lg text-xs font-semibold"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <p className="text-xs text-slate-400">No skills added yet.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;
