import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { driveApi } from '../../api/services';
import {
  PlusCircle,
  Briefcase,
  ShieldCheck,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Banknote,
  MapPin,
  FileText,
  Layers,
  ArrowRight,
} from 'lucide-react';

const PostDrive = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const [form, setForm] = useState({
    title: '',
    role_type: 'Full-Time',
    salary_package: '12 LPA',
    location: 'Bengaluru / Hybrid',
    job_description: '',
    requiredSkillsInput: 'Python, FastAPI, SQL, Docker, React',
    min_cgpa: 7.0,
    max_backlogs: 0,
    allowedProgrammesInput: 'B.Tech Computer Science, B.Tech IT, M.Tech CSE',
    allowedGradYearsInput: '2024, 2025, 2026',
    mandatorySkillsInput: 'Python, SQL',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    try {
      const required_skills = form.requiredSkillsInput
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean);

      const mandatory_skills = form.mandatorySkillsInput
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean);

      const allowed_programmes = form.allowedProgrammesInput
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean);

      const allowed_graduation_years = form.allowedGradYearsInput
        .split(',')
        .map((s) => parseInt(s.trim()))
        .filter((n) => !isNaN(n));

      const payload = {
        title: form.title,
        role_type: form.role_type,
        salary_package: form.salary_package,
        location: form.location,
        job_description: form.job_description,
        required_skills,
        eligibility_criteria: {
          min_cgpa: parseFloat(form.min_cgpa) || 0.0,
          max_backlogs: parseInt(form.max_backlogs) || 0,
          allowed_programmes,
          allowed_graduation_years,
          mandatory_skills,
        },
      };

      const created = await driveApi.createDrive(payload);
      setSuccessMsg('Placement drive successfully created, published, and synced to Neo4j graph!');
      setTimeout(() => {
        navigate('/recruiter/manage-drives');
      }, 1500);
    } catch (err) {
      console.error('Failed to post drive:', err);
      setErrorMsg(
        err.response?.data?.detail || 'Failed to create placement drive. Please check all fields.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h1 className="text-2xl font-extrabold text-slate-900">
          Post New Placement Drive
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
          Configure job specs, deterministic eligibility filters, and target skill graph requirements.
        </p>
      </div>

      {errorMsg && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-sm flex items-start gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-rose-600" />
          <div>
            <p className="font-bold">Error Creating Drive</p>
            <p className="text-xs mt-0.5">{errorMsg}</p>
          </div>
        </div>
      )}

      {successMsg && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 text-sm flex items-start gap-3">
          <CheckCircle2 className="w-5 h-5 shrink-0 mt-0.5 text-emerald-600" />
          <div>
            <p className="font-bold">Success</p>
            <p className="text-xs mt-0.5">{successMsg}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Core Job Details */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
            <Briefcase className="w-4 h-4 text-brand-600" />
            1. Role & Compensation
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                Job Title *
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Graduate Software Engineer"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                Role Type
              </label>
              <select
                value={form.role_type}
                onChange={(e) => setForm({ ...form, role_type: e.target.value })}
                className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
              >
                <option value="Full-Time">Full-Time</option>
                <option value="Internship">Internship</option>
                <option value="Contract">Contract</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                Salary Package / CTC *
              </label>
              <input
                type="text"
                required
                placeholder="e.g. 14 LPA or ₹50,000 / month"
                value={form.salary_package}
                onChange={(e) => setForm({ ...form, salary_package: e.target.value })}
                className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                Work Location
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Bengaluru / Hybrid / Remote"
                value={form.location}
                onChange={(e) => setForm({ ...form, location: e.target.value })}
                className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Job Description *
            </label>
            <textarea
              rows={4}
              required
              minLength={10}
              placeholder="Outline the responsibilities, tech stack, day-to-day tasks..."
              value={form.job_description}
              onChange={(e) => setForm({ ...form, job_description: e.target.value })}
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              All Targeted Required Skills (comma-separated)
            </label>
            <input
              type="text"
              placeholder="e.g. Python, FastAPI, Docker, PostgreSQL, React, Git"
              value={form.requiredSkillsInput}
              onChange={(e) => setForm({ ...form, requiredSkillsInput: e.target.value })}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
            />
            <p className="text-[11px] text-slate-400 mt-1">
              These skills will form <code className="bg-slate-100 px-1 py-0.5 rounded">(:PlacementDrive)-[:REQUIRES]-&gt;(:Skill)</code> edges and calculate candidate match percentages.
            </p>
          </div>
        </div>

        {/* Deterministic Eligibility Policy Filters */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            2. Deterministic Eligibility Policies (Strict Verification)
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Minimum CGPA Requirement (0.0 - 10.0)
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                required
                value={form.min_cgpa}
                onChange={(e) => setForm({ ...form, min_cgpa: e.target.value })}
                className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Maximum Active Backlogs Allowed
              </label>
              <input
                type="number"
                min="0"
                required
                value={form.max_backlogs}
                onChange={(e) => setForm({ ...form, max_backlogs: e.target.value })}
                className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Eligible Programmes / Degrees (comma-separated)
            </label>
            <input
              type="text"
              placeholder="e.g. B.Tech Computer Science, B.Tech IT, MCA"
              value={form.allowedProgrammesInput}
              onChange={(e) => setForm({ ...form, allowedProgrammesInput: e.target.value })}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Eligible Graduation Years (comma-separated)
            </label>
            <input
              type="text"
              placeholder="e.g. 2024, 2025, 2026"
              value={form.allowedGradYearsInput}
              onChange={(e) => setForm({ ...form, allowedGradYearsInput: e.target.value })}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div className="p-4 bg-indigo-50/50 border border-indigo-100 rounded-xl">
            <label className="block text-xs font-bold text-indigo-900 mb-1">
              Mandatory Skills (Must have 100% of these to be eligible)
            </label>
            <input
              type="text"
              placeholder="e.g. Python, SQL"
              value={form.mandatorySkillsInput}
              onChange={(e) => setForm({ ...form, mandatorySkillsInput: e.target.value })}
              className="w-full px-3.5 py-2 bg-white border border-indigo-200 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500"
            />
            <p className="text-[11px] text-indigo-700 mt-1">
              Unlike optional required skills, candidates who lack any mandatory skill will fail the policy check automatically.
            </p>
          </div>
        </div>

        {/* Submit */}
        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 bg-brand-600 hover:bg-brand-700 text-white font-bold text-sm rounded-xl shadow-lg shadow-brand-500/25 flex items-center gap-2 transition-all disabled:opacity-50"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <PlusCircle className="w-4 h-4" />
                <span>Publish Placement Drive</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PostDrive;
