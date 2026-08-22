import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { applicationApi } from '../../api/services';
import { StatusBadge } from '../../components/StatusBadge';
import {
  FileCheck2,
  Building2,
  Calendar,
  Sparkles,
  ArrowRight,
  Clock,
  CheckCircle,
  AlertCircle,
  MessageSquare,
} from 'lucide-react';

const MyApplications = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    setLoading(true);
    try {
      const data = await applicationApi.getMyApplications();
      setApplications(data || []);
    } catch (err) {
      console.error('Failed to fetch applications:', err);
    } finally {
      setLoading(false);
    }
  };

  const statusSteps = [
    'PENDING',
    'UNDER_REVIEW',
    'SHORTLISTED',
    'ASSESSMENT',
    'INTERVIEW',
    'SELECTED',
  ];

  const getStepIndex = (status) => {
    if (!status) return 0;
    const s = status.toUpperCase();
    if (s === 'REJECTED') return -1;
    return statusSteps.indexOf(s);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">
            Application Status Tracker
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Real-time status progression, match percentages, and recruiter audit remarks.
          </p>
        </div>
        <Link
          to="/student/drives"
          className="px-4 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-sm flex items-center gap-1.5"
        >
          Explore More Drives <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Applications List */}
      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-44 bg-slate-100 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : applications.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center shadow-sm">
          <FileCheck2 className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">No applications submitted yet</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            Browse our live placement drives, verify your eligibility with 1 click, and apply directly.
          </p>
          <Link
            to="/student/drives"
            className="mt-4 inline-block px-4 py-2 text-xs font-bold text-brand-600 bg-brand-50 hover:bg-brand-100 rounded-xl"
          >
            Explore Open Placement Drives →
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {applications.map((app) => {
            const currentStepIdx = getStepIndex(app.status);
            const isRejected = app.status?.toUpperCase() === 'REJECTED';

            return (
              <div
                key={app.id}
                className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6"
              >
                {/* Application Top Bar */}
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                  <div>
                    <span className="text-xs font-bold text-brand-600 uppercase tracking-wider">
                      {app.company_name}
                    </span>
                    <h3 className="text-lg font-bold text-slate-900 mt-0.5">
                      {app.drive_title}
                    </h3>
                    <div className="flex items-center gap-3 text-xs text-slate-500 mt-1">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5" />
                        Applied on {new Date(app.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">
                        Skill Match Score
                      </span>
                      <span className="text-sm font-black text-brand-600">
                        {app.match_percentage?.toFixed(1)}%
                      </span>
                    </div>
                    <StatusBadge status={app.status} />
                  </div>
                </div>

                {/* Progress Stepper Bar (if not rejected) */}
                {!isRejected ? (
                  <div className="hidden sm:block pt-2">
                    <div className="relative flex justify-between">
                      <div className="absolute top-1/2 left-0 w-full h-1 bg-slate-100 -translate-y-1/2 z-0" />
                      {statusSteps.map((step, idx) => {
                        const isCompleted = currentStepIdx >= idx;
                        const isCurrent = currentStepIdx === idx;

                        return (
                          <div
                            key={step}
                            className="relative z-10 flex flex-col items-center group"
                          >
                            <div
                              className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                                isCompleted
                                  ? 'bg-brand-600 text-white ring-4 ring-brand-100'
                                  : 'bg-white border-2 border-slate-200 text-slate-400'
                              }`}
                            >
                              {isCompleted ? <CheckCircle className="w-4 h-4" /> : idx + 1}
                            </div>
                            <span
                              className={`text-[10px] mt-1.5 font-bold uppercase tracking-wider ${
                                isCurrent
                                  ? 'text-brand-600'
                                  : isCompleted
                                  ? 'text-slate-700'
                                  : 'text-slate-400'
                              }`}
                            >
                              {step.replace('_', ' ')}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ) : (
                  <div className="p-3 bg-rose-50 border border-rose-100 rounded-xl flex items-center gap-2 text-xs text-rose-800">
                    <AlertCircle className="w-4 h-4 text-rose-600" />
                    <span>This application was marked as not selected. Check recruiter remarks below.</span>
                  </div>
                )}

                {/* Skills Match Overview */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs bg-slate-50 p-4 rounded-xl">
                  <div>
                    <span className="font-bold text-slate-700 block mb-1">
                      Matched Skills:
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {app.matched_skills?.map((s, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded font-semibold text-[11px]"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <span className="font-bold text-slate-700 block mb-1">
                      Skills to develop:
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {app.missing_skills?.map((s, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-0.5 bg-slate-200 text-slate-700 rounded text-[11px]"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Status Audit History & Remarks */}
                {app.status_history?.length > 0 && (
                  <div className="border-t border-slate-100 pt-4">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                      Review History & Recruiter Remarks
                    </h4>
                    <div className="space-y-2">
                      {app.status_history.map((hist, idx) => (
                        <div
                          key={idx}
                          className="flex items-start gap-2 text-xs text-slate-600 bg-white p-2.5 rounded-lg border border-slate-100"
                        >
                          <MessageSquare className="w-3.5 h-3.5 text-brand-500 mt-0.5 shrink-0" />
                          <div className="flex-1">
                            <span className="font-bold text-slate-800 mr-2">
                              Status changed to {hist.status}
                            </span>
                            {hist.remarks && (
                              <span className="text-slate-700 italic">"{hist.remarks}"</span>
                            )}
                            <span className="text-[10px] text-slate-400 block mt-0.5">
                              {new Date(hist.timestamp).toLocaleString()}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default MyApplications;
