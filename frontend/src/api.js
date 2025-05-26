// src/api.js
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE,
    timeout: 10000000,
});

export const generateDraft = async (topic) => {
    const res = await api.post('/generate', { topic });
    return res.data.draft;
};

export const publishDraft = async (draft) => {
    const res = await api.post('/publish', { draft });
    return res.data.url;
};

export const fetchMetrics = async (urn) => {
    const res = await api.get(`/metrics/${urn}`);
    return res.data;
};
