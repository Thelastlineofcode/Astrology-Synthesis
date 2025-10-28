import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const calculateChart = async (birthData, options = {}) => {
  const response = await api.post('/chart', { birthData, options });
  return response.data;
};

export const getZodiacInfo = async () => {
  const response = await api.get('/zodiac-info');
  return response.data;
};

export default api;
