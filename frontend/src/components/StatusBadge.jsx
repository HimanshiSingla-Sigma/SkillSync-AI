import React from 'react';

export const StatusBadge = ({ status }) => {
  const normalized = (status || '').toUpperCase();

  const styles = {
    PUBLISHED: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    DRAFT: 'bg-slate-100 text-slate-700 border-slate-200',
    CLOSED: 'bg-rose-50 text-rose-700 border-rose-200',
    COMPLETED: 'bg-blue-50 text-blue-700 border-blue-200',
    
    // Application statuses
    PENDING: 'bg-amber-50 text-amber-700 border-amber-200',
    UNDER_REVIEW: 'bg-blue-50 text-blue-700 border-blue-200',
    SHORTLISTED: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    ASSESSMENT: 'bg-purple-50 text-purple-700 border-purple-200',
    INTERVIEW: 'bg-cyan-50 text-cyan-700 border-cyan-200',
    SELECTED: 'bg-emerald-100 text-emerald-800 border-emerald-300 font-bold',
    REJECTED: 'bg-rose-50 text-rose-700 border-rose-200',

    // Eligibility
    ELIGIBLE: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    INELIGIBLE: 'bg-rose-50 text-rose-700 border-rose-200',
    PASS: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    FAIL: 'bg-rose-50 text-rose-700 border-rose-200',
  };

  const currentStyle = styles[normalized] || 'bg-slate-100 text-slate-700 border-slate-200';

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${currentStyle}`}
    >
      {normalized.replace('_', ' ')}
    </span>
  );
};
