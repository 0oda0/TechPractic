import axios from 'axios';
import { Document, SearchResponse } from '../types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

export const uploadDocument = async (file: File): Promise<any> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const getDocuments = async (): Promise<Document[]> => {
  const response = await api.get('/documents/documents');
  return response.data;
};

export const searchDocuments = async (query: string, page: number = 1, size: number = 10): Promise<SearchResponse> => {
  const response = await api.get('/search', { params: { q: query, page, size } });
  return response.data;
};