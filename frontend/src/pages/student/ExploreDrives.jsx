import React, { useState, useEffect } from 'react';
import { driveApi, eligibilityApi, applicationApi } from '../../api/services';
import Modal from '../../components/Modal';
import { StatusBadge } from '../../components/StatusBadge';
import {
  Search,
  Filter,
  Briefcase,
  Building2,
  MapPin,
  Banknote,
  ShieldCheck,
  ShieldAlert,
  CheckCircle,
  XCircle,
  Sparkles,
  ArrowRight,
  Clock,
  Layers,
  AlertCircle,
} from 'lucide-react';

const ExploreDrives = () => {
  const [drives, setDrives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSkill, setSelectedSkill] = useState('ALL');

  // Eligibility Evaluation Modal State
  const [eligibilityModalOpen, setEligibilityModalOpen] = useState(false);
  const [activeDrive, setActiveDrive] = useState(null);
  const [eligibilityResult, setEligibilityResult] = useState(null);
  const [checkingEligibility, setCheckingEligibility] = useState(false);

  // Application Submission State
  const [applying, setApplying] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState(null); // { type: 'success' | 'error', text: '' }

  useEffect(() => {
    fetchDrives();
  }, []);

  const fetchDrives = async () => {
    setLoading(true);
    try {
      const data = await driveApi.listDrives('PUBLISHED', 0, 100);
      setDrives(data || []);
    } catch (err) {
      console.error('Failed to fetch drives:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckEligibility = async (drive) => {
    setActiveDrive(drive);
    setEligibilityModalOpen(true);
    setCheckingEligibility(true);
    setEligibilityResult(null);
    setFeedbackMsg(null);

    try {
      const result = await eligibilityApi.checkEligibility(drive.id);
      setEligibilityResult(result);
    } catch (err) {
      console.error('Eligibility check error:', err);
      setEligibilityResult({
        error:
          err.response?.data?.detail ||
          'Could not run eligibility evaluation. Please ensure you are logged in.',
      });
    } finally {
      setCheckingEligibility(false);
    }
  };

  const handleApply = async (driveId) => {
    setApplying(true);
    setFeedbackMsg(null);
    try {
      await applicationApi.apply(driveId);
      setFeedbackMsg({
        type: 'success',
        text: 'Application successfully submitted! You can track status under "My Applications".',
      });
    } catch (err) {
      console.error('Application submission failed:', err);
      setFeedbackMsg({
        type: 'error',
        text:
          err.response?.data?.detail ||
          'Failed to submit application. Ensure you meet all deterministic criteria.',
      });
    } finally {
      setApplying(false);
    }
  };

  // Filter drives by search and skills
  const filteredDrives = drives.filter((d) => {
    const matchesSearch =
      d.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.company_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.required_skills?.some((s) => s.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesSkill =
      selectedSkill === 'ALL' ||
      d.required_skills?.some((s) => s.toLowerCase() === selectedSkill.toLowerCase());

    return matchesSearch && matchesSkill;
  });

  // Extract unique skills from all drives for quick filter pills
  const allSkills = Array.from(
    new Set(drives.flatMap((d) => d.required_skills || []))
  ).slice(0, 10);

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">
              Campus Placement Drives
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
              Explore active job postings with strict policy verification and skill graph matching.
            </p>
          </div>
          <span className="text-xs font-semibold px-3 py-1.5 bg-brand-50 text-brand-700 rounded-lg">
            {filteredDrives.length} Drives Available
          </span>
        </div>

        {/* Global Feedback Banner */}
        {feedbackMsg && (
          <div
            className={`p-4 rounded-xl text-sm flex items-start gap-3 ${
              feedbackMsg.type === 'success'
                ? 'bg-emerald-50 border border-emerald-200 text-emerald-800'
                : 'bg-rose-50 border border-rose-200 text-rose-800'
            }`}
          >
            {feedbackMsg.type === 'success' ? (
              <CheckCircle className="w-5 h-5 shrink-0 text-emerald-600 mt-0.5" />
            ) : (
              <AlertCircle className="w-5 h-5 shrink-0 text-rose-600 mt-0.5" />
            )}
            <div>
              <p className="font-bold">
                {feedbackMsg.type === 'success' ? 'Application Success' : 'Notice'}
              </p>
              <p className="text-xs mt-0.5">{feedbackMsg.text}</p>
            </div>
          </div>
        )}

        {/* Search Bar & Filters */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              placeholder="Search by role title, company name, or skill..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white"
            />
          </div>
        </div>

        {/* Quick Skill Filter Pills */}
        {allSkills.length > 0 && (
          <div className="flex flex-wrap items-center gap-1.5 pt-2">
            <span className="text-xs font-bold text-slate-400 mr-1 flex items-center gap-1">
              <Filter className="w-3 h-3" /> Filter:
            </span>
            <button
              onClick={() => setSelectedSkill('ALL')}
              className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                selectedSkill === 'ALL'
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              All Skills
            </button>
            {allSkills.map((skill) => (
              <button
                key={skill}
                onClick={() => setSelectedSkill(skill)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                  selectedSkill === skill
                    ? 'bg-brand-600 text-white shadow-sm'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {skill}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Drives Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-64 bg-slate-100 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : filteredDrives.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center shadow-sm">
          <Briefcase className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">No matching placement drives</h3>
          <p className="text-xs text-slate-500 mt-1">
            Try adjusting your search keywords or skill filters.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredDrives.map((drive) => (
            <div
              key={drive.id}
              className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
            >
              <div>
                {/* Header */}
                <div className="flex justify-between items-start">
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

                {/* Key specs */}
                <div className="flex flex-wrap gap-4 text-xs text-slate-600 my-3">
                  <div className="flex items-center gap-1.5">
                    <Banknote className="w-4 h-4 text-emerald-600" />
                    <span className="font-bold text-slate-900">{drive.salary_package}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <MapPin className="w-4 h-4 text-slate-400" />
                    <span>{drive.location}</span>
                  </div>
                </div>

                {/* Job Description Snippet */}
                <p className="text-xs text-slate-600 line-clamp-3 my-2 leading-relaxed">
                  {drive.job_description}
                </p>

                {/* Deterministic Criteria Pills */}
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 my-3 space-y-1 text-[11px] text-slate-600">
                  <div className="flex justify-between">
                    <span>Min CGPA:</span>
                    <strong className="text-slate-900">{drive.eligibility_criteria?.min_cgpa || 0}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Max Backlogs Allowed:</span>
                    <strong className="text-slate-900">{drive.eligibility_criteria?.max_backlogs ?? 0}</strong>
                  </div>
                  {drive.eligibility_criteria?.allowed_programmes?.length > 0 && (
                    <div className="flex justify-between">
                      <span>Eligible Branches:</span>
                      <span className="text-slate-900 font-medium truncate max-w-[180px]">
                        {drive.eligibility_criteria.allowed_programmes.join(', ')}
                      </span>
                    </div>
                  )}
                  {drive.eligibility_criteria?.mandatory_skills?.length > 0 && (
                    <div className="flex justify-between">
                      <span className="text-indigo-600 font-semibold">Mandatory Skills:</span>
                      <span className="text-indigo-700 font-bold truncate max-w-[180px]">
                        {drive.eligibility_criteria.mandatory_skills.join(', ')}
                      </span>
                    </div>
                  )}
                </div>

                {/* Skills */}
                <div className="flex flex-wrap gap-1.5 mt-2">
                  {drive.required_skills?.map((skill, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-md text-xs font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center gap-3">
                <button
                  onClick={() => handleCheckEligibility(drive)}
                  className="flex-1 py-2 px-3 text-xs font-bold text-brand-700 bg-brand-50 hover:bg-brand-100 border border-brand-200 rounded-xl transition-colors flex items-center justify-center gap-1.5"
                >
                  <ShieldCheck className="w-4 h-4 text-brand-600" />
                  Check Eligibility
                </button>

                <button
                  onClick={() => handleApply(drive.id)}
                  disabled={applying}
                  className="py-2 px-4 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-sm transition-all disabled:opacity-50 flex items-center gap-1"
                >
                  Apply
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Eligibility Evaluation Modal */}
      <Modal
        isOpen={eligibilityModalOpen}
        onClose={() => setEligibilityModalOpen(false)}
        title={activeDrive ? `Eligibility: ${activeDrive.title}` : 'Eligibility Evaluation'}
      >
        {checkingEligibility ? (
          <div className="py-12 flex flex-col items-center justify-center text-center space-y-3">
            <div className="w-10 h-10 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin" />
            <p className="text-sm font-semibold text-slate-800">
              Running Deterministic Policy Pipeline...
            </p>
            <p className="text-xs text-slate-500">
              Evaluating CGPA, Backlogs, Programme, and Neo4j Skill Overlap
            </p>
          </div>
        ) : eligibilityResult?.error ? (
          <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-sm">
            <p className="font-bold">Evaluation Error</p>
            <p className="text-xs mt-1">{eligibilityResult.error}</p>
          </div>
        ) : eligibilityResult ? (
          <div className="space-y-6">
            {/* Main Result Banner */}
            <div
              className={`p-5 rounded-2xl border flex items-center gap-4 ${
                eligibilityResult.eligible
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                  : 'bg-rose-50 border-rose-200 text-rose-900'
              }`}
            >
              <div
                className={`w-12 h-12 rounded-2xl flex items-center justify-center text-white ${
                  eligibilityResult.eligible ? 'bg-emerald-600' : 'bg-rose-600'
                }`}
              >
                {eligibilityResult.eligible ? (
                  <CheckCircle className="w-7 h-7" />
                ) : (
                  <XCircle className="w-7 h-7" />
                )}
              </div>
              <div>
                <h4 className="text-lg font-bold">
                  {eligibilityResult.eligible ? 'You Are Eligible!' : 'Not Eligible for this Drive'}
                </h4>
                <p className="text-xs mt-0.5 opacity-90">
                  {eligibilityResult.eligible
                    ? 'All strict policy checks passed. You can submit your application.'
                    : 'One or more deterministic placement criteria were not met.'}
                </p>
              </div>
            </div>

            {/* Skill Match Percentage Bar */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
              <div className="flex justify-between items-center text-xs font-bold text-slate-700 mb-1.5">
                <span>Skill Graph Overlap Score</span>
                <span className="text-brand-600 text-sm">
                  {eligibilityResult.match_percentage?.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-brand-500 to-indigo-600 h-2.5 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, eligibilityResult.match_percentage || 0)}%` }}
                />
              </div>
            </div>

            {/* Policy Breakdown Table */}
            <div>
              <h5 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
                Deterministic Policy Criteria Breakdown
              </h5>
              <div className="space-y-2">
                {eligibilityResult.policy_details &&
                  Object.entries(eligibilityResult.policy_details).map(([key, detail]) => (
                    <div
                      key={key}
                      className="p-3 bg-white border border-slate-200 rounded-xl flex items-start justify-between gap-3 text-xs"
                    >
                      <div>
                        <span className="font-bold text-slate-800 uppercase text-[11px] block">
                          {key.replace('_', ' ')} Check
                        </span>
                        <p className="text-slate-600 mt-0.5">{detail.message}</p>
                        {(detail.expected || detail.actual) && (
                          <p className="text-[10px] text-slate-400 mt-0.5">
                            Expected: {detail.expected} | Actual: {detail.actual}
                          </p>
                        )}
                      </div>
                      <StatusBadge status={detail.status} />
                    </div>
                  ))}
              </div>
            </div>

            {/* Matched vs Missing Skills */}
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div className="p-3 bg-emerald-50/60 border border-emerald-100 rounded-xl">
                <p className="font-bold text-emerald-800 mb-1.5 flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-600" /> Matched Skills (
                  {eligibilityResult.matched_skills?.length || 0})
                </p>
                <div className="flex flex-wrap gap-1">
                  {eligibilityResult.matched_skills?.map((s, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded text-[11px] font-semibold"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              <div className="p-3 bg-rose-50/60 border border-rose-100 rounded-xl">
                <p className="font-bold text-rose-800 mb-1.5 flex items-center gap-1">
                  <XCircle className="w-3.5 h-3.5 text-rose-600" /> Missing Skills (
                  {eligibilityResult.missing_skills?.length || 0})
                </p>
                <div className="flex flex-wrap gap-1">
                  {eligibilityResult.missing_skills?.map((s, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 bg-rose-100 text-rose-800 rounded text-[11px] font-semibold"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Modal Actions */}
            <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setEligibilityModalOpen(false)}
                className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
              >
                Close
              </button>
              {eligibilityResult.eligible && (
                <button
                  type="button"
                  onClick={() => {
                    handleApply(activeDrive.id);
                    setEligibilityModalOpen(false);
                  }}
                  disabled={applying}
                  className="px-5 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-md transition-all"
                >
                  Confirm & Apply
                </button>
              )}
            </div>
          </div>
        ) : null}
      </Modal>
    </div>
  );
};

export default ExploreDrives;
