import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { applicationApi, driveApi } from '../../api/services';
import { StatusBadge } from '../../components/StatusBadge';
import Modal from '../../components/Modal';
import {
  Users,
  Briefcase,
  ArrowLeft,
  CheckCircle2,
  AlertCircle,
  Clock,
  MessageSquare,
  Award,
  Sparkles,
  ChevronRight,
} from 'lucide-react';

const DriveApplicants = () => {
  const { driveId } = useParams();
  const [applicants, setApplicants] = useState([]);
  const [drive, setDrive] = useState(null);
  const [loading, setLoading] = useState(true);
  const [statusMsg, setStatusMsg] = useState(null);

  // Status Updater Modal State
  const [statusModalOpen, setStatusModalOpen] = useState(false);
  const [selectedApp, setSelectedApp] = useState(null);
  const [newStatus, setNewStatus] = useState('SHORTLISTED');
  const [remarks, setRemarks] = useState('');
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    fetchApplicantsAndDrive();
  }, [driveId]);

  const fetchApplicantsAndDrive = async () => {
    setLoading(true);
    try {
      const [driveInfo, appList] = await Promise.all([
        driveApi.getDrive(driveId).catch(() => null),
        applicationApi.getDriveApplicants(driveId).catch(() => []),
      ]);
      setDrive(driveInfo);
      setApplicants(appList || []);
    } catch (err) {
      console.error('Failed to load drive applicants:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenStatusModal = (app) => {
    setSelectedApp(app);
    setNewStatus(app.status || 'SHORTLISTED');
    setRemarks('');
    setStatusModalOpen(true);
  };

  const handleUpdateStatus = async (e) => {
    e.preventDefault();
    setUpdating(true);
    setStatusMsg(null);

    try {
      await applicationApi.updateStatus(selectedApp.id, newStatus, remarks);
      setStatusModalOpen(false);
      setStatusMsg({
        type: 'success',
        text: `Applicant status updated to ${newStatus} and recorded in Neo4j audit trail.`,
      });
      fetchApplicantsAndDrive();
    } catch (err) {
      console.error('Failed to update applicant status:', err);
      setStatusMsg({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to update applicant status.',
      });
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-2">
          <Link to="/recruiter/manage-drives" className="hover:text-brand-600 flex items-center gap-1">
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Drives
          </Link>
          <span>/</span>
          <span>Drive Applicants Pipeline</span>
        </div>

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900">
              {drive ? drive.title : 'Placement Drive Applicants'}
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
              Deterministic pre-screened candidates ranked by graph skill match overlap.
            </p>
          </div>
          <span className="px-3.5 py-1.5 bg-brand-50 text-brand-700 font-bold text-xs rounded-xl">
            {applicants.length} Total Applicants
          </span>
        </div>
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

      {/* Applicants Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-16 bg-slate-100 rounded-xl animate-pulse" />
            ))}
          </div>
        ) : applicants.length === 0 ? (
          <div className="p-12 text-center">
            <Users className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h3 className="text-base font-bold text-slate-800">No applicants yet</h3>
            <p className="text-xs text-slate-500 mt-1">
              Eligible students who meet your deterministic criteria will appear here once they apply.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase tracking-wider font-bold text-[11px]">
                  <th className="py-3.5 px-4">Student Candidate</th>
                  <th className="py-3.5 px-4">Academic Specs</th>
                  <th className="py-3.5 px-4">Graph Match %</th>
                  <th className="py-3.5 px-4">Matched Skills</th>
                  <th className="py-3.5 px-4">Current Status</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {applicants.map((app) => (
                  <tr key={app.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-4 px-4">
                      <p className="font-bold text-slate-900 text-sm">{app.student_name}</p>
                      <p className="text-slate-500 text-[11px]">{app.student_email}</p>
                    </td>

                    <td className="py-4 px-4">
                      <p className="font-semibold text-slate-800">CGPA: {app.student_cgpa}</p>
                      <p className="text-slate-500 text-[11px]">{app.student_branch}</p>
                    </td>

                    <td className="py-4 px-4">
                      <div className="flex items-center gap-2">
                        <span className="font-black text-brand-600 text-sm">
                          {app.match_percentage?.toFixed(1)}%
                        </span>
                      </div>
                    </td>

                    <td className="py-4 px-4 max-w-xs">
                      <div className="flex flex-wrap gap-1">
                        {app.matched_skills?.slice(0, 3).map((s, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-100 rounded text-[10px] font-semibold"
                          >
                            {s}
                          </span>
                        ))}
                        {(app.matched_skills?.length || 0) > 3 && (
                          <span className="text-[10px] text-slate-400 self-center">
                            +{(app.matched_skills?.length || 0) - 3} more
                          </span>
                        )}
                      </div>
                    </td>

                    <td className="py-4 px-4">
                      <StatusBadge status={app.status} />
                    </td>

                    <td className="py-4 px-4 text-right">
                      <button
                        onClick={() => handleOpenStatusModal(app)}
                        className="px-3 py-1.5 bg-brand-50 hover:bg-brand-100 text-brand-700 font-bold rounded-lg transition-colors inline-flex items-center gap-1"
                      >
                        <span>Update Status</span>
                        <ChevronRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Status Update Modal */}
      <Modal
        isOpen={statusModalOpen}
        onClose={() => setStatusModalOpen(false)}
        title={selectedApp ? `Review: ${selectedApp.student_name}` : 'Update Applicant Status'}
      >
        <form onSubmit={handleUpdateStatus} className="space-y-4">
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs text-slate-700">
            <p>
              Candidate: <strong className="text-slate-900">{selectedApp?.student_name}</strong>
            </p>
            <p className="mt-0.5">
              Current Status: <strong className="text-brand-600">{selectedApp?.status}</strong>
            </p>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Select New Hiring Pipeline Status
            </label>
            <select
              value={newStatus}
              onChange={(e) => setNewStatus(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm font-semibold focus:ring-2 focus:ring-brand-500"
            >
              <option value="UNDER_REVIEW">UNDER_REVIEW</option>
              <option value="SHORTLISTED">SHORTLISTED</option>
              <option value="ASSESSMENT">ASSESSMENT (Online Test)</option>
              <option value="INTERVIEW">INTERVIEW</option>
              <option value="SELECTED">SELECTED (Offer Extended)</option>
              <option value="REJECTED">REJECTED</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
              Reviewer Remarks / Feedback
            </label>
            <textarea
              rows={3}
              placeholder="e.g. Strong system design knowledge, clearing for technical round 2..."
              value={remarks}
              onChange={(e) => setRemarks(e.target.value)}
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-brand-500"
            />
          </div>

          <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setStatusModalOpen(false)}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={updating}
              className="px-5 py-2 text-xs font-bold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow transition-all disabled:opacity-50"
            >
              {updating ? 'Updating...' : 'Save & Update Neo4j Graph'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default DriveApplicants;
