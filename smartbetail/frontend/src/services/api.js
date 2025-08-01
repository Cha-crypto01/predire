import axios from 'axios';

// Configuration de base d'Axios
const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Erreur API:', error);
    return Promise.reject(error);
  }
);

// Services API pour SmartBétail
export const smartBetailAPI = {
  // Health check
  healthCheck: () => api.get('/health/'),

  // Dashboard
  getDashboardData: () => api.get('/dashboard/'),

  // Animaux
  getAnimals: (params = {}) => api.get('/animals/', { params }),
  getAnimal: (id) => api.get(`/animals/${id}/`),
  createAnimal: (data) => api.post('/animals/', data),
  updateAnimal: (id, data) => api.put(`/animals/${id}/`, data),
  deleteAnimal: (id) => api.delete(`/animals/${id}/`),

  // Maladies
  getDiseases: () => api.get('/diseases/'),
  getDisease: (id) => api.get(`/diseases/${id}/`),

  // Traitements
  getTreatments: () => api.get('/treatments/'),
  getTreatment: (id) => api.get(`/treatments/${id}/`),

  // Symptômes observés
  getSymptoms: (params = {}) => api.get('/symptoms/', { params }),
  createSymptom: (data) => api.post('/symptoms/', data),

  // Diagnostics
  getDiagnostics: (params = {}) => api.get('/diagnostics/', { params }),
  getDiagnostic: (id) => api.get(`/diagnostics/${id}/`),

  // Planification des soins
  getSchedule: (params = {}) => api.get('/schedule/', { params }),
  createSchedule: (data) => api.post('/schedule/', data),
  updateSchedule: (id, data) => api.put(`/schedule/${id}/`, data),
  deleteSchedule: (id) => api.delete(`/schedule/${id}/`),
  getOverdueSchedule: () => api.get('/schedule/en_retard/'),
  getWeeklySchedule: () => api.get('/schedule/cette_semaine/'),

  // Prédiction IA
  predictDisease: (data) => api.post('/predict/', data),

  // Recommandations de traitement
  recommendTreatment: (data) => api.post('/recommend/', data),
};

// Utilitaires pour les erreurs
export const getErrorMessage = (error) => {
  if (error.response?.data?.error) {
    return error.response.data.error;
  }
  if (error.response?.data?.errors) {
    const errors = error.response.data.errors;
    const errorMessages = Object.entries(errors)
      .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
      .join('; ');
    return errorMessages;
  }
  if (error.message) {
    return error.message;
  }
  return 'Une erreur inattendue est survenue';
};

// Hook personnalisé pour les appels API avec gestion d'état
import { useState, useCallback } from 'react';

export const useAPI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const callAPI = useCallback(async (apiCall, ...args) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiCall(...args);
      setLoading(false);
      return response.data;
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      setLoading(false);
      throw err;
    }
  }, []);

  return { callAPI, loading, error, setError };
};

export default api;