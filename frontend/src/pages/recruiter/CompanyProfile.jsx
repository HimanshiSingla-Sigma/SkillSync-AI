import React, { useState, useEffect } from 'react';
import { companyApi } from '../../api/services';
import { useAuth } from '../../context/AuthContext';
import {
  Building2,
  Globe,
  MapPin,
  Save,
  CheckCircle2,
  AlertCircle,
  FileText,
} from 'lucide-react';

const CompanyProfile = () => {
  const { user, refreshUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState(null);

  const [form, setForm] = useState({
    name: '',
    industry: '',
    website: '',
    location: '',
    description: '',
  });

  useEffect(() => {
    if (user) {
      setForm({
        name: user.name || '',
        industry: user.industry || 'Information Technology',
        website: user.website || '',
        location: user.location || '',
        description: user.description || '',
      });
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatusMsg(null);

    try {
      await companyApi.updateMyProfile(form);
      await refreshUser();
      setStatusMsg({
        type: 'success',
        text: 'Company recruiter profile successfully updated and synchronized to Neo4j!',
      });
    } catch (err) {
      console.error('Failed to update company profile:', err);
      setStatusMsg({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to update company profile.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h1 className="text-2xl font-extrabold text-slate-900">
          Company & Recruiter Profile
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
          Public details visible to students discovering your active placement drives.
        </p>
      </div>

      {statusMsg && (
        <div
          className={`p-4 rounded-xl text-sm flex items-start gap-3 ${
            statusMsg.type === 'success'
              ? 'bg-emerald-50 border border-emerald-200 text-emerald-800'
              : 'bg-rose-50 border border-rose-200 text-rose-800'
          }`}
        >
          {statusMsg.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-600 mt-0.5" />
          ) : (
            <AlertCircle className="w-5 h-5 shrink-0 text-rose-600 mt-0.5" />
          )}
          <div>
            <p className="font-bold">{statusMsg.type === 'success' ? 'Success' : 'Error'}</p>
            <p className="text-xs mt-0.5">{statusMsg.text}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
            Company Official Name *
          </label>
          <div className="relative">
            <Building2 className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              required
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Industry Domain
            </label>
            <input
              type="text"
              required
              value={form.industry}
              onChange={(e) => setForm({ ...form, industry: e.target.value })}
              className="w-full px-3.5 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Headquarters / Location
            </label>
            <div className="relative">
              <MapPin className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="text"
                value={form.location}
                onChange={(e) => setForm({ ...form, location: e.target.value })}
                className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
              />
            </div>
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
            Official Website
          </label>
          <div className="relative">
            <Globe className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="url"
              placeholder="https://company.example.com"
              value={form.website}
              onChange={(e) => setForm({ ...form, website: e.target.value })}
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
            Company Overview & Mission
          </label>
          <textarea
            rows={4}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
          />
        </div>

        <div className="flex justify-end pt-4 border-t border-slate-100">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white font-bold text-sm rounded-xl shadow-md shadow-brand-500/20 flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>Save Company Profile</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default CompanyProfile;
