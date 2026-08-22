import React, { useState, useEffect } from 'react';
import { resumeApi } from '../../api/services';
import { useAuth } from '../../context/AuthContext';
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  Edit3,
  Plus,
  Trash2,
  GraduationCap,
  Briefcase,
  Layers,
  Save,
  Check,
} from 'lucide-react';

const ResumeStudio = () => {
  const { refreshUser } = useAuth();
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [statusMsg, setStatusMsg] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  // Edit form state
  const [editForm, setEditForm] = useState({
    extracted_name: '',
    extracted_email: '',
    extracted_phone: '',
    extracted_skills: [],
    skillsInput: '',
  });

  useEffect(() => {
    fetchResume();
  }, []);

  const fetchResume = async () => {
    setLoading(true);
    try {
      const data = await resumeApi.getMyResume();
      setResume(data);
      if (data) {
        setEditForm({
          extracted_name: data.extracted_name || '',
          extracted_email: data.extracted_email || '',
          extracted_phone: data.extracted_phone || '',
          extracted_skills: data.extracted_skills || [],
          skillsInput: '',
        });
      }
    } catch (err) {
      console.warn('No resume found or error fetching:', err);
      setResume(null);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0] || selectedFile;
    if (!file) return;

    setUploading(true);
    setStatusMsg(null);

    try {
      const res = await resumeApi.uploadResume(file);
      setResume(res);
      setStatusMsg({
        type: 'success',
        text: 'Resume successfully uploaded, parsed, and synced to Neo4j knowledge graph!',
      });
      await refreshUser();
    } catch (err) {
      console.error('Upload failed:', err);
      setStatusMsg({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to upload and parse resume file.',
      });
    } finally {
      setUploading(false);
      setSelectedFile(null);
    }
  };

  const handleAddSkill = () => {
    if (!editForm.skillsInput.trim()) return;
    const newSkills = editForm.skillsInput
      .split(',')
      .map((s) => s.trim())
      .filter((s) => s && !editForm.extracted_skills.includes(s));

    setEditForm({
      ...editForm,
      extracted_skills: [...editForm.extracted_skills, ...newSkills],
      skillsInput: '',
    });
  };

  const handleRemoveSkill = (skillToRemove) => {
    setEditForm({
      ...editForm,
      extracted_skills: editForm.extracted_skills.filter((s) => s !== skillToRemove),
    });
  };

  const handleSaveCorrections = async () => {
    setStatusMsg(null);
    try {
      const payload = {
        extracted_name: editForm.extracted_name,
        extracted_email: editForm.extracted_email,
        extracted_phone: editForm.extracted_phone,
        extracted_skills: editForm.extracted_skills,
      };
      const updated = await resumeApi.correctResume(payload);
      setResume(updated);
      setIsEditing(false);
      setStatusMsg({
        type: 'success',
        text: 'Resume modifications synchronized with MongoDB and Neo4j graph nodes.',
      });
      await refreshUser();
    } catch (err) {
      console.error('Failed to correct resume:', err);
      setStatusMsg({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to save corrections.',
      });
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">
            Resume Studio & Parser
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Automated PDF/DOCX entity extraction, skill lexicon mapping, and knowledge graph sync.
          </p>
        </div>
        {resume && (
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="px-4 py-2 text-xs font-bold text-brand-600 bg-brand-50 hover:bg-brand-100 rounded-xl flex items-center gap-1.5 transition-colors"
          >
            <Edit3 className="w-4 h-4" />
            {isEditing ? 'Cancel Editing' : 'Adjust Parsed Data'}
          </button>
        )}
      </div>

      {/* Status Messages */}
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
            <p className="font-bold">{statusMsg.type === 'success' ? 'Success' : 'Notice'}</p>
            <p className="text-xs mt-0.5">{statusMsg.text}</p>
          </div>
        </div>
      )}

      {/* Upload Zone */}
      <div className="bg-white p-8 rounded-2xl border-2 border-dashed border-slate-300 hover:border-brand-500 text-center transition-colors">
        <UploadCloud className="w-12 h-12 text-brand-500 mx-auto mb-3" />
        <h3 className="text-base font-bold text-slate-800">
          Upload your Resume (PDF or DOCX)
        </h3>
        <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
          Our parser extracts contact details, education history, projects, and skills to establish
          graph edges in Neo4j automatically.
        </p>

        <div className="mt-5 flex justify-center items-center gap-3">
          <label className="cursor-pointer px-5 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold rounded-xl shadow-md shadow-brand-500/20 transition-all flex items-center gap-2">
            <FileText className="w-4 h-4" />
            <span>Select File</span>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileUpload}
              className="hidden"
              disabled={uploading}
            />
          </label>
        </div>

        {uploading && (
          <div className="mt-4 flex items-center justify-center gap-2 text-xs font-semibold text-brand-600">
            <div className="w-4 h-4 border-2 border-brand-300 border-t-brand-600 rounded-full animate-spin" />
            <span>Extracting text & mapping skills to Neo4j...</span>
          </div>
        )}
      </div>

      {/* Parsed Resume Breakdown View */}
      {loading ? (
        <div className="h-64 bg-slate-100 rounded-2xl animate-pulse" />
      ) : resume ? (
        <div className="space-y-6">
          {/* Top Extracted Info Card */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <div className="flex justify-between items-start mb-4">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Parsed Contact Entity
                </span>
                <h3 className="text-xl font-bold text-slate-900 mt-0.5">
                  {resume.extracted_name || 'Name not detected'}
                </h3>
              </div>
              <span className="px-3 py-1 bg-brand-50 text-brand-700 rounded-full text-xs font-bold">
                {resume.file_name}
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-slate-600">
              <div className="p-3 bg-slate-50 rounded-xl">
                <span className="font-semibold text-slate-400 block text-[10px] uppercase">
                  Detected Email:
                </span>
                <span className="font-medium text-slate-800 text-sm">
                  {resume.extracted_email || 'None detected'}
                </span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl">
                <span className="font-semibold text-slate-400 block text-[10px] uppercase">
                  Detected Phone:
                </span>
                <span className="font-medium text-slate-800 text-sm">
                  {resume.extracted_phone || 'None detected'}
                </span>
              </div>
            </div>
          </div>

          {/* Skills Section & Graph Representation */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <div>
                <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-brand-600" />
                  Canonical Extracted Skills ({resume.extracted_skills?.length || 0})
                </h3>
                <p className="text-xs text-slate-500">
                  These skills form active <code className="bg-slate-100 px-1 py-0.5 rounded">(:Student)-[:HAS_SKILL]-&gt;(:Skill)</code> graph relationships.
                </p>
              </div>
            </div>

            {isEditing ? (
              <div className="space-y-4 p-4 bg-brand-50/50 rounded-xl border border-brand-100">
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Add skills (e.g. Docker, PyTorch, GraphQL)..."
                    value={editForm.skillsInput}
                    onChange={(e) =>
                      setEditForm({ ...editForm, skillsInput: e.target.value })
                    }
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleAddSkill();
                      }
                    }}
                    className="flex-1 px-3 py-2 bg-white border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-brand-500"
                  />
                  <button
                    type="button"
                    onClick={handleAddSkill}
                    className="px-3 py-2 bg-brand-600 text-white rounded-xl text-xs font-bold"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>

                <div className="flex flex-wrap gap-2">
                  {editForm.extracted_skills.map((skill, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 bg-white border border-brand-200 text-brand-700 rounded-lg text-xs font-semibold flex items-center gap-1.5"
                    >
                      {skill}
                      <button
                        type="button"
                        onClick={() => handleRemoveSkill(skill)}
                        className="text-rose-500 hover:text-rose-700"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>

                <div className="flex justify-end pt-2">
                  <button
                    onClick={handleSaveCorrections}
                    className="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold rounded-xl shadow flex items-center gap-1.5"
                  >
                    <Save className="w-3.5 h-3.5" />
                    Save & Sync to Neo4j
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                {resume.extracted_skills?.map((skill, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1.5 bg-brand-50 border border-brand-100 text-brand-700 rounded-xl text-xs font-bold shadow-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Education & Experience & Projects Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Education */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
              <h4 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                <GraduationCap className="w-4 h-4 text-indigo-600" />
                Parsed Education
              </h4>
              {resume.extracted_education?.length ? (
                <div className="space-y-3">
                  {resume.extracted_education.map((edu, idx) => (
                    <div key={idx} className="p-3 bg-slate-50 rounded-xl text-xs space-y-1">
                      <p className="font-bold text-slate-900">{edu.degree || 'Degree'}</p>
                      <p className="text-slate-600">{edu.university || edu.branch}</p>
                      {edu.graduation_year && (
                        <p className="text-[11px] text-slate-400">Class of {edu.graduation_year}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400">No education sections detected.</p>
              )}
            </div>

            {/* Projects */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
              <h4 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                <Layers className="w-4 h-4 text-purple-600" />
                Parsed Projects
              </h4>
              {resume.extracted_projects?.length ? (
                <div className="space-y-3">
                  {resume.extracted_projects.map((proj, idx) => (
                    <div key={idx} className="p-3 bg-slate-50 rounded-xl text-xs space-y-1">
                      <p className="font-bold text-slate-900">{proj.title}</p>
                      {proj.description && (
                        <p className="text-slate-600 line-clamp-2">{proj.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400">No project sections detected.</p>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center shadow-sm">
          <FileText className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">No Resume Uploaded Yet</h3>
          <p className="text-xs text-slate-500 mt-1">
            Upload your resume above to extract skills and enable deterministic placement matches.
          </p>
        </div>
      )}
    </div>
  );
};

export default ResumeStudio;
