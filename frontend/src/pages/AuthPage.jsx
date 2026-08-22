import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  GraduationCap,
  Building2,
  Lock,
  Mail,
  User,
  Sparkles,
  ArrowRight,
  AlertCircle,
  CheckCircle,
  Briefcase,
  Layers,
  Globe,
  MapPin,
} from 'lucide-react';

const AuthPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { loginStudent, registerStudent, loginRecruiter, registerRecruiter, isAuthenticated, isStudent, isRecruiter } = useAuth();

  // Mode: 'login' | 'register'
  const [mode, setMode] = useState(searchParams.get('mode') === 'register' ? 'register' : 'login');
  // Role: 'student' | 'recruiter'
  const [role, setRole] = useState(searchParams.get('role') === 'recruiter' ? 'recruiter' : 'student');

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // Student Form State
  const [studentForm, setStudentForm] = useState({
    email: '',
    password: '',
    full_name: '',
    cgpa: 7.5,
    backlogs: 0,
    programme: 'B.Tech Computer Science',
    branch: 'Computer Science',
    graduation_year: 2025,
    skillsInput: 'Python, React, FastApi, SQL',
  });

  // Recruiter Form State
  const [recruiterForm, setRecruiterForm] = useState({
    name: '',
    email: '',
    password: '',
    industry: 'Information Technology',
    website: 'https://company.example.com',
    location: 'Bengaluru / Remote',
    description: 'Leading technology & AI software enterprise.',
  });

  useEffect(() => {
    if (isAuthenticated) {
      if (isStudent) navigate('/student/dashboard');
      else if (isRecruiter) navigate('/recruiter/dashboard');
    }
  }, [isAuthenticated, isStudent, isRecruiter, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    try {
      if (role === 'student') {
        if (mode === 'login') {
          await loginStudent(studentForm.email, studentForm.password);
          navigate('/student/dashboard');
        } else {
          // Register Student
          const payload = {
            email: studentForm.email,
            password: studentForm.password,
            full_name: studentForm.full_name,
            cgpa: parseFloat(studentForm.cgpa) || 0.0,
            backlogs: parseInt(studentForm.backlogs) || 0,
            programme: studentForm.programme,
            branch: studentForm.branch,
            graduation_year: parseInt(studentForm.graduation_year) || 2025,
            skills: studentForm.skillsInput
              .split(',')
              .map((s) => s.trim())
              .filter(Boolean),
          };
          await registerStudent(payload);
          navigate('/student/dashboard');
        }
      } else {
        // Recruiter
        if (mode === 'login') {
          await loginRecruiter(recruiterForm.email, recruiterForm.password);
          navigate('/recruiter/dashboard');
        } else {
          // Register Recruiter
          await registerRecruiter(recruiterForm);
          navigate('/recruiter/dashboard');
        }
      }
    } catch (err) {
      console.error('Auth error:', err);
      const detail =
        err.response?.data?.detail ||
        (typeof err.response?.data === 'string' ? err.response?.data : null) ||
        'Authentication failed. Please check your credentials.';
      setErrorMsg(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-4 sm:p-6 bg-slate-50">
      <div className="w-full max-w-xl bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">
        {/* Top Gradient Header */}
        <div className="bg-gradient-to-r from-brand-700 via-indigo-600 to-purple-600 p-6 text-white text-center">
          <div className="w-12 h-12 mx-auto rounded-2xl bg-white/10 backdrop-blur-md flex items-center justify-center mb-3 shadow-inner">
            <Sparkles className="w-6 h-6 text-indigo-200" />
          </div>
          <h2 className="text-2xl font-bold">
            {mode === 'login' ? 'Welcome Back' : 'Create an Account'}
          </h2>
          <p className="text-indigo-100 text-sm mt-1">
            Access CareerConnect AI Placement & GraphRAG Platform
          </p>

          {/* Role Switcher Tabs */}
          <div className="flex bg-black/20 p-1 rounded-xl max-w-xs mx-auto mt-5">
            <button
              type="button"
              onClick={() => {
                setRole('student');
                setErrorMsg('');
              }}
              className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                role === 'student'
                  ? 'bg-white text-brand-700 shadow'
                  : 'text-indigo-100 hover:text-white'
              }`}
            >
              <GraduationCap className="w-4 h-4" />
              Student
            </button>
            <button
              type="button"
              onClick={() => {
                setRole('recruiter');
                setErrorMsg('');
              }}
              className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                role === 'recruiter'
                  ? 'bg-white text-brand-700 shadow'
                  : 'text-indigo-100 hover:text-white'
              }`}
            >
              <Building2 className="w-4 h-4" />
              Recruiter / Company
            </button>
          </div>
        </div>

        {/* Form Body */}
        <div className="p-6 sm:p-8">
          {errorMsg && (
            <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-start gap-3">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">Authentication Error</p>
                <p className="text-xs mt-0.5">{errorMsg}</p>
              </div>
            </div>
          )}

          {successMsg && (
            <div className="mb-6 p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm flex items-start gap-3">
              <CheckCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold">Success</p>
                <p className="text-xs mt-0.5">{successMsg}</p>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {role === 'student' ? (
              // ================= STUDENT FIELDS =================
              <>
                {mode === 'register' && (
                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                      Full Name
                    </label>
                    <div className="relative">
                      <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                      <input
                        type="text"
                        required
                        placeholder="e.g. Alex Johnson"
                        value={studentForm.full_name}
                        onChange={(e) =>
                          setStudentForm({ ...studentForm, full_name: e.target.value })
                        }
                        className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white"
                      />
                    </div>
                  </div>
                )}

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Student Email
                  </label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                    <input
                      type="email"
                      required
                      placeholder="student@university.edu"
                      value={studentForm.email}
                      onChange={(e) =>
                        setStudentForm({ ...studentForm, email: e.target.value })
                      }
                      className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                    <input
                      type="password"
                      required
                      minLength={6}
                      placeholder="••••••••"
                      value={studentForm.password}
                      onChange={(e) =>
                        setStudentForm({ ...studentForm, password: e.target.value })
                      }
                      className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white"
                    />
                  </div>
                </div>

                {mode === 'register' && (
                  <>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-bold text-slate-600 mb-1">
                          CGPA (0.0 - 10.0)
                        </label>
                        <input
                          type="number"
                          step="0.01"
                          min="0"
                          max="10"
                          required
                          value={studentForm.cgpa}
                          onChange={(e) =>
                            setStudentForm({ ...studentForm, cgpa: e.target.value })
                          }
                          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-bold text-slate-600 mb-1">
                          Active Backlogs
                        </label>
                        <input
                          type="number"
                          min="0"
                          required
                          value={studentForm.backlogs}
                          onChange={(e) =>
                            setStudentForm({ ...studentForm, backlogs: e.target.value })
                          }
                          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-bold text-slate-600 mb-1">
                          Programme
                        </label>
                        <input
                          type="text"
                          required
                          value={studentForm.programme}
                          onChange={(e) =>
                            setStudentForm({ ...studentForm, programme: e.target.value })
                          }
                          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-bold text-slate-600 mb-1">
                          Grad Year
                        </label>
                        <input
                          type="number"
                          min="2020"
                          max="2035"
                          required
                          value={studentForm.graduation_year}
                          onChange={(e) =>
                            setStudentForm({ ...studentForm, graduation_year: e.target.value })
                          }
                          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-600 mb-1">
                        Initial Skills (comma-separated)
                      </label>
                      <input
                        type="text"
                        placeholder="Python, React, FastAPI, SQL, Docker"
                        value={studentForm.skillsInput}
                        onChange={(e) =>
                          setStudentForm({ ...studentForm, skillsInput: e.target.value })
                        }
                        className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                      />
                    </div>
                  </>
                )}
              </>
            ) : (
              // ================= RECRUITER FIELDS =================
              <>
                {mode === 'register' && (
                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                      Company Name
                    </label>
                    <div className="relative">
                      <Building2 className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                      <input
                        type="text"
                        required
                        placeholder="e.g. Acme Technologies Inc."
                        value={recruiterForm.name}
                        onChange={(e) =>
                          setRecruiterForm({ ...recruiterForm, name: e.target.value })
                        }
                        className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white"
                      />
                    </div>
                  </div>
                )}

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Recruiter Work Email
                  </label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                    <input
                      type="email"
                      required
                      placeholder="recruiter@company.com"
                      value={recruiterForm.email}
                      onChange={(e) =>
                        setRecruiterForm({ ...recruiterForm, email: e.target.value })
                      }
                      className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                    <input
                      type="password"
                      required
                      minLength={6}
                      placeholder="••••••••"
                      value={recruiterForm.password}
                      onChange={(e) =>
                        setRecruiterForm({ ...recruiterForm, password: e.target.value })
                      }
                      className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white"
                    />
                  </div>
                </div>

                {mode === 'register' && (
                  <>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="block text-xs font-bold text-slate-600 mb-1">
                          Industry
                        </label>
                        <input
                          type="text"
                          required
                          value={recruiterForm.industry}
                          onChange={(e) =>
                            setRecruiterForm({ ...recruiterForm, industry: e.target.value })
                          }
                          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-bold text-slate-600 mb-1">
                          Location
                        </label>
                        <input
                          type="text"
                          required
                          value={recruiterForm.location}
                          onChange={(e) =>
                            setRecruiterForm({ ...recruiterForm, location: e.target.value })
                          }
                          className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-600 mb-1">
                        Company Website
                      </label>
                      <input
                        type="url"
                        value={recruiterForm.website}
                        onChange={(e) =>
                          setRecruiterForm({ ...recruiterForm, website: e.target.value })
                        }
                        className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                      />
                    </div>
                  </>
                )}
              </>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-6 py-3 px-4 bg-brand-600 hover:bg-brand-700 text-white font-semibold rounded-xl shadow-lg shadow-brand-500/25 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <span>
                    {mode === 'login'
                      ? `Sign In as ${role === 'student' ? 'Student' : 'Recruiter'}`
                      : `Register as ${role === 'student' ? 'Student' : 'Recruiter'}`}
                  </span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Toggle Login / Register */}
          <div className="mt-6 pt-6 border-t border-slate-100 text-center">
            {mode === 'login' ? (
              <p className="text-sm text-slate-600">
                Don't have an account yet?{' '}
                <button
                  type="button"
                  onClick={() => {
                    setMode('register');
                    setErrorMsg('');
                  }}
                  className="font-bold text-brand-600 hover:text-brand-700 underline"
                >
                  Create one now
                </button>
              </p>
            ) : (
              <p className="text-sm text-slate-600">
                Already registered?{' '}
                <button
                  type="button"
                  onClick={() => {
                    setMode('login');
                    setErrorMsg('');
                  }}
                  className="font-bold text-brand-600 hover:text-brand-700 underline"
                >
                  Sign In here
                </button>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
