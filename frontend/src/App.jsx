import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import ProtectedRoute from './components/ProtectedRoute';

// Public Pages
import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';

// Student Pages
import StudentDashboard from './pages/student/StudentDashboard';
import ExploreDrives from './pages/student/ExploreDrives';
import ResumeStudio from './pages/student/ResumeStudio';
import MyApplications from './pages/student/MyApplications';
import AIChatAssistant from './pages/student/AIChatAssistant';
import StudentProfile from './pages/student/StudentProfile';

// Recruiter Pages
import RecruiterDashboard from './pages/recruiter/RecruiterDashboard';
import PostDrive from './pages/recruiter/PostDrive';
import ManageDrives from './pages/recruiter/ManageDrives';
import DriveApplicants from './pages/recruiter/DriveApplicants';
import CompanyProfile from './pages/recruiter/CompanyProfile';

// Shared Dashboard Shell Layout
const DashboardLayout = () => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <div className="bg-gradient-to-r from-indigo-900 via-purple-900 to-slate-900 text-white px-4 py-2 text-center text-xs sm:text-sm font-medium flex items-center justify-center gap-3 shadow-lg border-b border-indigo-500/30">
        <span>✨ <strong>Looking for the new Animated GraphRAG Platform?</strong> It runs directly from the backend server!</span>
        <a 
          href="http://localhost:8000" 
          className="bg-indigo-500 hover:bg-indigo-600 text-white font-bold px-3 py-1 rounded-full text-xs transition duration-200 shadow"
        >
          Open Modern Platform (Port 8000) →
        </a>
      </div>
      <Navbar />
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        <Sidebar />
        <main className="flex-1 p-4 sm:p-6 lg:p-8 min-w-0 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

// Public Layout with Navbar
const PublicLayout = () => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public Routes */}
          <Route element={<PublicLayout />}>
            <Route path="/" element={<LandingPage />} />
            <Route path="/auth" element={<AuthPage />} />
          </Route>

          {/* Student Protected Portal */}
          <Route
            path="/student"
            element={
              <ProtectedRoute allowedRoles={['STUDENT', 'ADMIN']}>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route path="dashboard" element={<StudentDashboard />} />
            <Route path="drives" element={<ExploreDrives />} />
            <Route path="resume" element={<ResumeStudio />} />
            <Route path="applications" element={<MyApplications />} />
            <Route path="chat" element={<AIChatAssistant />} />
            <Route path="profile" element={<StudentProfile />} />
            <Route index element={<Navigate to="dashboard" replace />} />
          </Route>

          {/* Recruiter Protected Portal */}
          <Route
            path="/recruiter"
            element={
              <ProtectedRoute allowedRoles={['RECRUITER', 'COMPANY', 'ADMIN']}>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route path="dashboard" element={<RecruiterDashboard />} />
            <Route path="manage-drives" element={<ManageDrives />} />
            <Route path="post-drive" element={<PostDrive />} />
            <Route path="drive/:driveId/applicants" element={<DriveApplicants />} />
            <Route path="profile" element={<CompanyProfile />} />
            <Route index element={<Navigate to="dashboard" replace />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
