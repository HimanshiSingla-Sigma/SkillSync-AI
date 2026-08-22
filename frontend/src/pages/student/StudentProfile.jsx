import React, { useState, useEffect } from 'react';
import { studentApi } from '../../api/services';
import { useAuth } from '../../context/AuthContext';
import {
  User,
  GraduationCap,
  Layers,
  Sparkles,
  Save,
  CheckCircle2,
  AlertCircle,
  Plus,
  Trash2,
  Github,
  Linkedin,
  Phone,
  BookOpen,
} from 'lucide-react';

const StudentProfile = () => {
  const { user, refreshUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState(null);

  // Form State
  const [profileForm, setProfileForm] = useState({
    full_name: '',
    cgpa: 0.0,
    backlogs: 0,
    programme: '',
    branch: '',
    graduation_year: 2025,
    phone: '',
    bio: '',
    github_url: '',
    linkedin_url: '',
  });

  const [skills, setSkills] = useState([]);
  const [newSkillInput, setNewSkillInput] = useState('');

  useEffect(() => {
    if (user) {
      setProfileForm({
        full_name: user.full_name || '',
        cgpa: user.profile?.cgpa ?? 0.0,
        backlogs: user.profile?.backlogs ?? 0,
        programme: user.profile?.programme || 'B.Tech Computer Science',
        branch: user.profile?.branch || 'Computer Science',
        graduation_year: user.profile?.graduation_year || 2025,
        phone: user.profile?.phone || '',
        bio: user.profile?.bio || '',
        github_url: user.profile?.github_url || '',
        linkedin_url: user.profile?.linkedin_url || '',
      });
      setSkills(user.skills || []);
    }
  }, [user]);

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatusMsg(null);

    try {
      const payload = {
        full_name: profileForm.full_name,
        profile: {
          cgpa: parseFloat(profileForm.cgpa) || 0.0,
          backlogs: parseInt(profileForm.backlogs) || 0,
          programme: profileForm.programme,
          branch: profileForm.branch,
          graduation_year: parseInt(profileForm.graduation_year) || 2025,
          phone: profileForm.phone,
          bio: profileForm.bio,
          github_url: profileForm.github_url,
          linkedin_url: profileForm.linkedin_url,
        },
      };

      await studentApi.updateProfile(payload);
      await refreshUser();
      setStatusMsg({
        type: 'success',
        text: 'Profile attributes and deterministic eligibility parameters successfully updated!',
      });
    } catch (err) {
      console.error('Update profile error:', err);
      setStatusMsg({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to update student profile.',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAddSkill = async () => {
    if (!newSkillInput.trim()) return;
    const added = newSkillInput
      .split(',')
      .map((s) => s.trim())
      .filter((s) => s && !skills.includes(s));

    const updatedSkills = [...skills, ...added];
    setSkills(updatedSkills);
    setNewSkillInput('');

    try {
      await studentApi.updateSkills(updatedSkills);
      await refreshUser();
      setStatusMsg({
        type: 'success',
        text: 'Skill nodes added and synchronized to Neo4j placement graph!',
      });
    } catch (err) {
      console.error('Failed to update skills:', err);
    }
  };

  const handleRemoveSkill = async (skillToRemove) => {
    const updatedSkills = skills.filter((s) => s !== skillToRemove);
    setSkills(updatedSkills);

    try {
      await studentApi.updateSkills(updatedSkills);
      await refreshUser();
      setStatusMsg({
        type: 'success',
        text: 'Skill relationship updated in Neo4j knowledge graph.',
      });
    } catch (err) {
      console.error('Failed to update skills:', err);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h1 className="text-2xl font-extrabold text-slate-900">
          Student Profile & Placement Criteria
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
          These parameters strictly determine your pass/fail status against recruiter policies.
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
            <p className="font-bold">{statusMsg.type === 'success' ? 'Saved' : 'Error'}</p>
            <p className="text-xs mt-0.5">{statusMsg.text}</p>
          </div>
        </div>
      )}

      {/* Skills Manager Card */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-brand-600" />
              Your Skill Graph Nodes ({skills.length})
            </h3>
            <p className="text-xs text-slate-500">
              Synced directly to Neo4j for placement multi-hop matching
            </p>
          </div>
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Add skills (e.g. Python, Docker, FastApi, React)..."
            value={newSkillInput}
            onChange={(e) => setNewSkillInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleAddSkill();
              }
            }}
            className="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
          />
          <button
            type="button"
            onClick={handleAddSkill}
            className="px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs rounded-xl shadow flex items-center gap-1.5"
          >
            <Plus className="w-4 h-4" /> Add Skill
          </button>
        </div>

        <div className="flex flex-wrap gap-2 pt-2">
          {skills.map((skill, idx) => (
            <span
              key={idx}
              className="px-3 py-1 bg-brand-50 border border-brand-100 text-brand-700 rounded-xl text-xs font-bold flex items-center gap-2 shadow-2xs"
            >
              {skill}
              <button
                type="button"
                onClick={() => handleRemoveSkill(skill)}
                className="text-slate-400 hover:text-rose-600"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Main Profile Form */}
      <form onSubmit={handleUpdateProfile} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3">
          Academic & Personal Parameters
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Full Name
            </label>
            <input
              type="text"
              required
              value={profileForm.full_name}
              onChange={(e) =>
                setProfileForm({ ...profileForm, full_name: e.target.value })
              }
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Email Address
            </label>
            <input
              type="email"
              disabled
              value={user?.email || ''}
              className="w-full px-3.5 py-2.5 bg-slate-100 border border-slate-200 rounded-xl text-sm text-slate-500 cursor-not-allowed"
            />
          </div>
        </div>

        {/* Academic Policy Parameters */}
        <div className="p-4 bg-brand-50/40 border border-brand-100 rounded-2xl space-y-4">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-700 block">
            Placement Criteria Fields
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                CGPA (0.0 - 10.0)
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                required
                value={profileForm.cgpa}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, cgpa: e.target.value })
                }
                className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 font-bold text-slate-900"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Active Backlogs
              </label>
              <input
                type="number"
                min="0"
                required
                value={profileForm.backlogs}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, backlogs: e.target.value })
                }
                className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 font-bold text-slate-900"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Graduation Year
              </label>
              <input
                type="number"
                min="2020"
                max="2035"
                required
                value={profileForm.graduation_year}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, graduation_year: e.target.value })
                }
                className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 font-bold text-slate-900"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Branch
              </label>
              <input
                type="text"
                required
                value={profileForm.branch}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, branch: e.target.value })
                }
                className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 font-bold text-slate-900"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Degree / Programme
            </label>
            <input
              type="text"
              required
              value={profileForm.programme}
              onChange={(e) =>
                setProfileForm({ ...profileForm, programme: e.target.value })
              }
              className="w-full px-3 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 font-medium text-slate-900"
            />
          </div>
        </div>

        {/* Links & Contact */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              LinkedIn Profile URL
            </label>
            <div className="relative">
              <Linkedin className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="url"
                placeholder="https://linkedin.com/in/..."
                value={profileForm.linkedin_url}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, linkedin_url: e.target.value })
                }
                className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              GitHub Profile URL
            </label>
            <div className="relative">
              <Github className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="url"
                placeholder="https://github.com/..."
                value={profileForm.github_url}
                onChange={(e) =>
                  setProfileForm({ ...profileForm, github_url: e.target.value })
                }
                className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
              />
            </div>
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
            Short Bio
          </label>
          <textarea
            rows={3}
            placeholder="Tell recruiters about your key strengths and interests..."
            value={profileForm.bio}
            onChange={(e) =>
              setProfileForm({ ...profileForm, bio: e.target.value })
            }
            className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 focus:bg-white"
          />
        </div>

        <div className="flex justify-end pt-4 border-t border-slate-100">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2.5 bg-brand-600 hover:bg-brand-700 text-white font-bold text-sm rounded-xl shadow-md shadow-brand-500/20 transition-all flex items-center gap-2 disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>Save Profile Parameters</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default StudentProfile;
