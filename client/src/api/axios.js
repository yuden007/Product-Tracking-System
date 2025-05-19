import axios from 'axios';

// Set default base URL (replace with your Flask backend URL)
const api = axios.create({
  baseURL: 'http://localhost:5000', // Flask default URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
