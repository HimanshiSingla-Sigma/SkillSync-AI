import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { driveApi, companyApi } from '../../api/services';
import { useAuth } from '../../context/AuthContext';
import { StatusBadge } from '../../components/StatusBadge';
import {
  Building2,
  Briefcase,
  Users,
  PlusCircle,
  Sparkles,
  ArrowRight,
  TrendingUp,
  Award,
  Layers,
  MapPin,
  Globe,
} from 'lucide-react';

const RecruiterDashboard = () => {
  const { user } = useAuth();
  const [drives, setDrives] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecruiterData = async () => {
      try {
        const myDrives = await driveApi.getMyDrives();
        setDrives(myDrives || []);
      } catch (err) {
        console.error('Failed to load recruiter drives:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecruiterData();
  }, []);

  const totalDrives = drives.length;
  const activeDrives = drives.filter((d) => d.status === 'PUBLISHED').length;

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-brand-950 rounded-3xl p-6 sm:p-8 text-white shadow-xl shadow-slate-900/10 relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-xs font-semibold uppercase tracking-wider mb-3">
            <Building2 className="w-3.5 h-3.5 text-indigo-300" />
            Recruiter & Enterprise Command Center
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome, {user?.name || 'Recruiter'}
          </h1>
          <p className="text-indigo-100 text-sm sm:text-base mt-2">
            Manage your campus recruitment drives, configure deterministic policy filters (CGPA,
            backlogs, mandatory skills), and evaluate applicants with AI graph match scores.
          </p>

          <div className="flex flex-wrap gap-3 mt-5">
            <Link
              to="/recruiter/post-drive"
              className="px-4 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5"
            >
              <PlusCircle className="w-4 h-4" />
              Post New Placement Drive
            </Link>
            <Link
              to="/recruiter/manage-drives"
              className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-xs rounded-xl transition-all flex items-center gap-1.5"
            >
              <Briefcase className="w-4 h-4" />
              Manage Existing Drives
            </Link>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Total Posted Drives
            </span>
            <div className="p-2 bg-brand-50 text-brand-600 rounded-xl">
              <Briefcase className="w-4 h-4" />
            </div>
          </div>
          <p className="text-3xl font-black text-slate-900 mt-2">{totalDrives}</p>
          <p className="text-xs text-slate-500 mt-1">Configured in MongoDB & Neo4j</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Active Hiring Drives
            </span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <p className="text-3xl font-black text-slate-900 mt-2">{activeDrives}</p>
          <p className="text-xs text-slate-500 mt-1">Published and accepting candidates</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Company Location
            </span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-xl">
              <Building2 className="w-4 h-4" />
            </div>
          </div>
          <p className="text-base font-bold text-slate-900 mt-3 truncate">
            {user?.location || 'Bengaluru / Remote'}
          </p>
          <p className="text-xs text-slate-500 mt-1">{user?.industry || 'Technology'}</p>
        </div>
      </div>

      {/* Posted Drives Table */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Your Placement Drives</h2>
            <p className="text-xs text-slate-500">
              Review applicant lists, match percentages, and update candidate hiring status
            </p>
          </div>
          <Link
            to="/recruiter/post-drive"
            className="px-3.5 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl flex items-center gap-1.5 shadow-sm"
          >
            <PlusCircle className="w-4 h-4" />
            Create Drive
          </Link>
        </div>

        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-20 bg-slate-100 rounded-xl animate-pulse" />
            ))}
          </div>
        ) : drives.length === 0 ? (
          <div className="text-center py-12">
            <Briefcase className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-800">No recruitment drives posted yet</h3>
            <p className="text-xs text-slate-500 mt-1">
              Create your first placement drive to begin receiving pre-screened eligible applicants.
            </p>
            <Link
              to="/recruiter/post-drive"
              className="mt-4 inline-block px-4 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl"
            >
              Post Drive Now →
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {drives.map((drive) => (
              <div
                key={drive.id}
                className="py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:bg-slate-50/60 p-3 rounded-xl transition-all"
              >
                <div>
                  <div className="flex items-center gap-2.5">
                    <h3 className="text-sm font-bold text-slate-900">{drive.title}</h3>
                    <StatusBadge status={drive.status} />
                  </div>
                  <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-1.5">
                    <span>Package: <strong className="text-slate-800">{drive.salary_package}</strong></span>
                    <span>•</span>
                    <span>Role: {drive.role_type}</span>
                    <span>•</span>
                    <span>Min CGPA: {drive.eligibility_criteria?.min_cgpa || 0}</span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Link
                    to={`/recruiter/drive/${drive.id}/applicants`}
                    className="px-3.5 py-1.5 text-xs font-bold text-brand-700 bg-brand-50 hover:bg-brand-100 border border-brand-200 rounded-xl flex items-center gap-1.5 transition-colors"
                  >
                    <Users className="w-3.5 h-3.5 text-brand-600" />
                    View Applicants
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecruiterDashboard;
