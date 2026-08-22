import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { driveApi } from '../api/services';
import {
  Sparkles,
  ShieldCheck,
  GitFork,
  FileCheck2,
  Bot,
  ArrowRight,
  CheckCircle2,
  Building2,
  GraduationCap,
  Briefcase,
  TrendingUp,
  MapPin,
  Banknote,
} from 'lucide-react';

const LandingPage = () => {
  const [featuredDrives, setFeaturedDrives] = useState([]);
  const [loadingDrives, setLoadingDrives] = useState(true);

  useEffect(() => {
    const fetchDrives = async () => {
      try {
        const data = await driveApi.listDrives('PUBLISHED', 0, 4);
        setFeaturedDrives(data);
      } catch (err) {
        console.warn('Could not fetch public drives:', err);
      } finally {
        setLoadingDrives(false);
      }
    };
    fetchDrives();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-indigo-950 via-slate-900 to-slate-950 text-white pt-20 pb-24 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 opacity-20 bg-[radial-gradient(#6366f1_1px,transparent_1px)] [background-size:16px_16px]" />
        
        <div className="relative max-w-5xl mx-auto text-center space-y-8">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-400/30 text-indigo-300 text-xs font-semibold tracking-wide uppercase shadow-inner">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            Dual-Engine: MongoDB + Neo4j GraphRAG
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
            Intelligent Placement &{' '}
            <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400 bg-clip-text text-transparent">
              SkillSync AI Platform
            </span>
          </h1>

          <p className="max-w-3xl mx-auto text-lg sm:text-xl text-slate-300 font-normal leading-relaxed">
            Eliminate placement ambiguity with deterministic policy checks, automated resume skill extraction, 
            and graph-augmented generative AI for students and campus recruiters.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link
              to="/auth?mode=register&role=student"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl text-base font-semibold text-white bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 shadow-lg shadow-brand-500/25 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5"
            >
              <GraduationCap className="w-5 h-5" />
              Join as Student
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              to="/auth?mode=register&role=recruiter"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl text-base font-semibold text-slate-200 bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 flex items-center justify-center gap-2 transition-all"
            >
              <Building2 className="w-5 h-5 text-indigo-400" />
              Recruiter Portal
            </Link>
          </div>

          {/* Key Feature Badges */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-12 text-left">
            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60 backdrop-blur-sm">
              <ShieldCheck className="w-6 h-6 text-emerald-400 mb-2" />
              <h4 className="text-sm font-bold text-white">Deterministic Rules</h4>
              <p className="text-xs text-slate-400 mt-1">Zero-hallucination CGPA, backlog, and branch checks</p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60 backdrop-blur-sm">
              <GitFork className="w-6 h-6 text-indigo-400 mb-2" />
              <h4 className="text-sm font-bold text-white">Neo4j Graph Engine</h4>
              <p className="text-xs text-slate-400 mt-1">Multi-hop skill graphs connecting students & drives</p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60 backdrop-blur-sm">
              <FileCheck2 className="w-6 h-6 text-purple-400 mb-2" />
              <h4 className="text-sm font-bold text-white">Smart Resume Parser</h4>
              <p className="text-xs text-slate-400 mt-1">Automated PDF/DOCX skill taxonomy extraction</p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60 backdrop-blur-sm">
              <Bot className="w-6 h-6 text-pink-400 mb-2" />
              <h4 className="text-sm font-bold text-white">GraphRAG AI Chat</h4>
              <p className="text-xs text-slate-400 mt-1">Grounded placement guidance with graph context</p>
            </div>
          </div>
        </div>
      </section>

      {/* Live Featured Drives Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 w-full">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-end mb-8 gap-4">
          <div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              Live Recruitment Drives
            </h2>
            <p className="text-slate-600 text-sm mt-1">
              Actively hiring companies with deterministic eligibility criteria
            </p>
          </div>
          <Link
            to="/student/drives"
            className="text-sm font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1.5 group"
          >
            Explore all drives
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {loadingDrives ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[1, 2].map((i) => (
              <div key={i} className="h-44 bg-slate-200/70 rounded-2xl animate-pulse" />
            ))}
          </div>
        ) : featuredDrives.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
            <Briefcase className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-800">No active placement drives yet</h3>
            <p className="text-sm text-slate-500 mt-1">Recruiters will publish new drives soon.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {featuredDrives.map((drive) => (
              <div
                key={drive.id}
                className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between"
              >
                <div>
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <span className="text-xs font-bold text-brand-600 uppercase tracking-wider">
                        {drive.company_name}
                      </span>
                      <h3 className="text-lg font-bold text-slate-900 mt-0.5">
                        {drive.title}
                      </h3>
                    </div>
                    <span className="px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-xs font-semibold">
                      {drive.role_type}
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-4 text-xs text-slate-600 my-3">
                    <div className="flex items-center gap-1.5">
                      <Banknote className="w-3.5 h-3.5 text-slate-400" />
                      <span className="font-semibold text-slate-900">{drive.salary_package}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      <span>{drive.location}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <ShieldCheck className="w-3.5 h-3.5 text-indigo-500" />
                      <span>Min CGPA: {drive.eligibility_criteria?.min_cgpa || 0}</span>
                    </div>
                  </div>

                  {/* Skills tags */}
                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {drive.required_skills?.slice(0, 4).map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded-md text-xs font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                    {(drive.required_skills?.length || 0) > 4 && (
                      <span className="text-xs text-slate-400 self-center">
                        +{(drive.required_skills?.length || 0) - 4} more
                      </span>
                    )}
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-100 flex justify-between items-center">
                  <span className="text-xs text-slate-400">
                    Max Backlogs Allowed: {drive.eligibility_criteria?.max_backlogs ?? 0}
                  </span>
                  <Link
                    to="/student/drives"
                    className="px-4 py-1.5 text-xs font-semibold text-brand-600 bg-brand-50 hover:bg-brand-100 rounded-lg transition-colors"
                  >
                    View & Apply
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Footer */}
      <footer className="mt-auto bg-slate-900 text-slate-400 py-10 px-4 text-center border-t border-slate-800 text-sm">
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2 font-bold text-white">
            <Sparkles className="w-4 h-4 text-brand-400" />
            CareerConnect AI / SkillSync AI
          </div>
          <p className="text-xs text-slate-500">
            Powered by FastAPI, MongoDB, Neo4j Graph Database, and Ollama GraphRAG
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
