import axios from 'axios';
import type { Resume, InterviewSession, AnswerResponse } from '../types';

// Connect to your local Python Backend
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Upload Resume
  uploadResume: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    // We use generics <Resume> to tell TypeScript what the result looks like
    const response = await apiClient.post<Resume>('/upload-resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  // Start Interview
  startInterview: async (resumeId: number) => {
    const response = await apiClient.post<InterviewSession>(`/start/${resumeId}`);
    return response.data;
  },

  // Submit Audio Answer
  submitAnswer: async (sessionId: number, question: string, audioBlob: Blob) => {
    const formData = new FormData();
    // The backend expects the file to be named 'file'
    formData.append('file', audioBlob, 'answer.wav'); 
    
    // We send the 'question' as a query parameter for Context Injection
    const response = await apiClient.post<AnswerResponse>(
      `/${sessionId}/answer?question=${encodeURIComponent(question)}`, 
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    return response.data;
  }
};