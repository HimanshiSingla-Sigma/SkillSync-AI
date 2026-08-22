import apiClient from './client';

// ==========================================
// Authentication APIs (Student & Recruiter)
// ==========================================
export const authApi = {
  studentRegister: async (data) => {
    const res = await apiClient.post('/students/register', data);
    return res.data;
  },
  studentLogin: async (data) => {
    const res = await apiClient.post('/students/login', data);
    return res.data;
  },
  companyRegister: async (data) => {
    const res = await apiClient.post('/companies/register', data);
    return res.data;
  },
  companyLogin: async (data) => {
    const res = await apiClient.post('/companies/login', data);
    return res.data;
  },
};

// ==========================================
// Student APIs
// ==========================================
export const studentApi = {
  getProfile: async () => {
    const res = await apiClient.get('/students/profile/me');
    return res.data;
  },
  updateProfile: async (data) => {
    const res = await apiClient.put('/students/profile/me', data);
    return res.data;
  },
  updateSkills: async (skills) => {
    const res = await apiClient.put('/students/profile/me/skills', { skills });
    return res.data;
  },
  getById: async (studentId) => {
    const res = await apiClient.get(`/students/${studentId}`);
    return res.data;
  },
  listAll: async (skip = 0, limit = 100) => {
    const res = await apiClient.get('/students/', { params: { skip, limit } });
    return res.data;
  },
};

// ==========================================
// Company & Recruiter APIs
// ==========================================
export const companyApi = {
  getMyProfile: async () => {
    const res = await apiClient.get('/companies/profile/me');
    return res.data;
  },
  updateMyProfile: async (data) => {
    const res = await apiClient.put('/companies/profile/me', data);
    return res.data;
  },
  listAll: async (skip = 0, limit = 100) => {
    const res = await apiClient.get('/companies/public', { params: { skip, limit } });
    return res.data;
  },
  getById: async (companyId) => {
    const res = await apiClient.get(`/companies/${companyId}`);
    return res.data;
  },
};

// ==========================================
// Placement Drives APIs
// ==========================================
export const driveApi = {
  listDrives: async (status = 'PUBLISHED', skip = 0, limit = 100) => {
    const res = await apiClient.get('/drives/', { params: { status, skip, limit } });
    return res.data;
  },
  getMyDrives: async () => {
    const res = await apiClient.get('/drives/company/my-drives');
    return res.data;
  },
  getDrive: async (driveId) => {
    const res = await apiClient.get(`/drives/${driveId}`);
    return res.data;
  },
  createDrive: async (data) => {
    const res = await apiClient.post('/drives/', data);
    return res.data;
  },
  updateDrive: async (driveId, data) => {
    const res = await apiClient.put(`/drives/${driveId}`, data);
    return res.data;
  },
};

// ==========================================
// Deterministic Eligibility Policy APIs
// ==========================================
export const eligibilityApi = {
  checkEligibility: async (driveId) => {
    const res = await apiClient.get(`/eligibility/check/${driveId}`);
    return res.data;
  },
};

// ==========================================
// Applications APIs
// ==========================================
export const applicationApi = {
  apply: async (driveId) => {
    const res = await apiClient.post('/applications/apply', { drive_id: driveId });
    return res.data;
  },
  getMyApplications: async () => {
    const res = await apiClient.get('/applications/student/my-applications');
    return res.data;
  },
  getDriveApplicants: async (driveId) => {
    const res = await apiClient.get(`/applications/drive/${driveId}/applicants`);
    return res.data;
  },
  updateStatus: async (applicationId, status, remarks = '') => {
    const res = await apiClient.put(`/applications/${applicationId}/status`, {
      status,
      remarks,
    });
    return res.data;
  },
};

// ==========================================
// Resume Processing & Parsing APIs
// ==========================================
export const resumeApi = {
  uploadResume: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },
  getMyResume: async () => {
    const res = await apiClient.get('/resumes/me');
    return res.data;
  },
  correctResume: async (data) => {
    const res = await apiClient.put('/resumes/me/correct', data);
    return res.data;
  },
};

// ==========================================
// AI Career Assistant & GraphRAG APIs
// ==========================================
export const chatApi = {
  askAssistant: async (question, driveId = null) => {
    const payload = { question };
    if (driveId) {
      payload.drive_id = driveId;
    }
    const res = await apiClient.post('/chat/ask', payload);
    return res.data;
  },
  getFAQs: async () => {
    const res = await apiClient.get('/chat/faqs');
    return res.data;
  },
};

// ==========================================
// System Health Check
// ==========================================
export const healthApi = {
  checkHealth: async () => {
    const res = await apiClient.get('/health');
    return res.data;
  },
};
