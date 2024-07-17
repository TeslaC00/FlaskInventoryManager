import axios from 'axios';
import { getToken } from '../utils/token';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000/api', // Replace with your API base URL
});

axiosInstance.interceptors.request.use(
  config => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

export default axiosInstance;