import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { driveApi } from '../../api/services';
import { StatusBadge } from '../../components/StatusBadge';
import Modal from '../../components/Modal';
import {
  Briefcase,
  Users,
  PlusCircle,
  Edit2,
  CheckCircle2,
  AlertCircle,
  Eye,
  MapPin,
  Banknote,
  ShieldCheck,
} from 'lucide-react';

const ManageDrives = () => {
  const [drives, setDrives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusMsg, setStatusMsg] = useState(null);

  // Edit Modal State
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [selectedDrive, setSelectedDrive] = useState(null);
  const [editForm, setEditForm] = useState({
    title: '',
    role_type: '',
    salary_package: '',
    location: '',
    job_description: '',
    status: 'PUBLISHED',
  });
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    fetchDrives();
  }, []);

  const fetchDrives = async () => {
    setLoading(true);
    try {
      const data = await driveApi.getMyDrives();
      setDrives(data || []);
    } catch (err) {
      console.error('Failed to load company drives:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenEdit = (drive) => {
    setSelectedDrive(drive);
    setEditForm({
      title: drive.title,
      role_type: drive.role_type,
      salary_package: drive.salary_package,
      location: drive.location,
      job_description: drive.job_description,
      status: drive.status,
    });
    setEditModalOpen(true);
  };

  const handleUpdateDrive = async (e) => {
    e.preventDefault();
    setUpdating(true);
    setStatusMsg(null);

    try {
      await driveApi.updateDrive(selectedDrive.id, editForm);
      setEditModalOpen(false);
      setStatusMsg({
        type: 'success',
        text: 'Placement drive successfully updated and synced!',
      });
      fetchDrives();
    } catch (err) {
      console.error('Failed to update drive:', err);
      setStatusMsg({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to update drive details.',
      });
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">
            Manage Placement Drives
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            View active listings, inspect candidate applicant pipelines, and manage statuses.
          </p>
        </div>
        <Link
          to="/recruiter/post-drive"
          className="px-4 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow flex items-center gap-1.5"
        >
          <PlusCircle className="w-4 h-4" />
          Post New Drive
        </Link>
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

      {/* Drives List */}
      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-44 bg-slate-100 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : drives.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center shadow-sm">
          <Briefcase className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">No recruitment drives posted yet</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            Create your first drive to begin evaluating pre-screened student talent.
          </p>
          <Link
            to="/recruiter/post-drive"
            className="mt-4 inline-block px-4 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl"
          >
            Post Drive Now →
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {drives.map((drive) => (
            <div
              key={drive.id}
              className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6"
            >
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-3">
                  <h3 className="text-lg font-bold text-slate-900">{drive.title}</h3>
                  <StatusBadge status={drive.status} />
                </div>

                <div className="flex flex-wrap items-center gap-4 text-xs text-slate-600">
                  <div className="flex items-center gap-1">
                    <Banknote className="w-3.5 h-3.5 text-emerald-600" />
                    <span className="font-bold text-slate-900">{drive.salary_package}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    <span>{drive.location}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
                    <span>Min CGPA: {drive.eligibility_criteria?.min_cgpa || 0}</span>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1.5 pt-1">
                  {drive.required_skills?.map((s, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded text-xs font-medium"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
                <button
                  onClick={() => handleOpenEdit(drive)}
                  className="px-3.5 py-2 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl flex items-center gap-1.5 transition-colors"
                >
                  <Edit2 className="w-3.5 h-3.5" />
                  Edit Details
                </button>

                <Link
                  to={`/recruiter/drive/${drive.id}/applicants`}
                  className="px-4 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-sm flex items-center gap-1.5 transition-all"
                >
                  <Users className="w-3.5 h-3.5" />
                  View Applicants
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Edit Modal */}
      <Modal
        isOpen={editModalOpen}
        onClose={() => setEditModalOpen(false)}
        title="Edit Placement Drive"
      >
        <form onSubmit={handleUpdateDrive} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Job Title
            </label>
            <input
              type="text"
              required
              value={editForm.title}
              onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 font-medium"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                Salary Package
              </label>
              <input
                type="text"
                required
                value={editForm.salary_package}
                onChange={(e) =>
                  setEditForm({ ...editForm, salary_package: e.target.value })
                }
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 font-medium"
              />
            </div>
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                Status
              </label>
              <select
                value={editForm.status}
                onChange={(e) => setEditForm({ ...editForm, status: e.target.value })}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500 font-semibold"
              >
                <option value="PUBLISHED">PUBLISHED (Accepting Applicants)</option>
                <option value="DRAFT">DRAFT</option>
                <option value="CLOSED">CLOSED</option>
                <option value="COMPLETED">COMPLETED</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Location
            </label>
            <input
              type="text"
              value={editForm.location}
              onChange={(e) => setEditForm({ ...editForm, location: e.target.value })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Job Description
            </label>
            <textarea
              rows={4}
              value={editForm.job_description}
              onChange={(e) =>
                setEditForm({ ...editForm, job_description: e.target.value })
              }
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setEditModalOpen(false)}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={updating}
              className="px-5 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow transition-all disabled:opacity-50"
            >
              {updating ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default ManageDrives;
