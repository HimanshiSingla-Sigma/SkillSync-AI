import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi, studentApi, companyApi } from '../api/services';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [role, setRole] = useState(localStorage.getItem('role') || null);
  const [loading, setLoading] = useState(true);

  // Initialize auth state from storage on mount
  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem('token');
      const savedRole = localStorage.getItem('role');
      const savedUser = localStorage.getItem('user');

      if (savedToken && savedRole) {
        setToken(savedToken);
        setRole(savedRole);
        if (savedUser) {
          try {
            setUser(JSON.parse(savedUser));
          } catch (e) {
            console.error('Failed to parse cached user', e);
          }
        }
        // Fetch fresh profile from backend
        try {
          if (savedRole === 'STUDENT') {
            const profile = await studentApi.getProfile();
            setUser(profile);
            localStorage.setItem('user', JSON.stringify(profile));
          } else if (savedRole === 'RECRUITER' || savedRole === 'COMPANY') {
            const profile = await companyApi.getMyProfile();
            setUser(profile);
            localStorage.setItem('user', JSON.stringify(profile));
          }
        } catch (error) {
          console.warn('Could not refresh profile on load:', error);
        }
      }
      setLoading(false);
    };

    initAuth();

    // Listen for unauthorized events to auto-logout
    const handleUnauthorized = () => {
      logout();
    };
    window.addEventListener('auth:unauthorized', handleUnauthorized);
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized);
  }, []);

  const saveAuthSession = (tokenVal, userObj, userRole) => {
    setToken(tokenVal);
    setUser(userObj);
    setRole(userRole);
    localStorage.setItem('token', tokenVal);
    localStorage.setItem('role', userRole);
    localStorage.setItem('user', JSON.stringify(userObj));
  };

  const loginStudent = async (email, password) => {
    const res = await authApi.studentLogin({ email, password });
    saveAuthSession(res.access_token, res.student, 'STUDENT');
    return res;
  };

  const registerStudent = async (data) => {
    const res = await authApi.studentRegister(data);
    saveAuthSession(res.access_token, res.student, 'STUDENT');
    return res;
  };

  const loginRecruiter = async (email, password) => {
    const res = await authApi.companyLogin({ email, password });
    saveAuthSession(res.access_token, res.company, 'RECRUITER');
    return res;
  };

  const registerRecruiter = async (data) => {
    const res = await authApi.companyRegister(data);
    saveAuthSession(res.access_token, res.company, 'RECRUITER');
    return res;
  };

  const refreshUser = async () => {
    try {
      if (role === 'STUDENT') {
        const profile = await studentApi.getProfile();
        setUser(profile);
        localStorage.setItem('user', JSON.stringify(profile));
        return profile;
      } else if (role === 'RECRUITER') {
        const profile = await companyApi.getMyProfile();
        setUser(profile);
        localStorage.setItem('user', JSON.stringify(profile));
        return profile;
      }
    } catch (e) {
      console.error('Failed to refresh user:', e);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    setRole(null);
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        role,
        loading,
        isAuthenticated: !!token && !!user,
        isStudent: role === 'STUDENT',
        isRecruiter: role === 'RECRUITER',
        loginStudent,
        registerStudent,
        loginRecruiter,
        registerRecruiter,
        refreshUser,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
