import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, Loader2, ArrowRight } from 'lucide-react';
import { api } from '../api/client';
import type { Resume } from '../types';

export const Welcome = () => {
  const navigate = useNavigate(); // <--- Hook for navigation
  const [loading, setLoading] = useState(false);
  const [starting, setStarting] = useState(false); // New loading state for start button
  const [resume, setResume] = useState<Resume | null>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    try {
      const data = await api.uploadResume(file);
      setResume(data);
    } catch (err) {
      console.error(err);
      alert("Failed to upload. Is the Backend running?");
    } finally {
      setLoading(false);
    }
  };

  // --- NEW LOGIC TO START INTERVIEW ---
  const handleStartInterview = async () => {
    if (!resume) return;
    setStarting(true);
    try {
        // 1. Ask Backend to generate questions
        const session = await api.startInterview(resume.id);
        
        // 2. Navigate to Interview Page
        // We pass the 'questions' in the state so we don't need to fetch them again
        navigate(`/interview/${session.session_id}`, { 
            state: { questions: session.questions } 
        });
    } catch (err) {
        console.error(err);
        alert("Failed to start interview.");
    } finally {
        setStarting(false);
    }
  };
  // ------------------------------------

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="max-w-2xl w-full space-y-8">
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="h-16 w-16 bg-blue-100 rounded-full flex items-center justify-center">
              <FileText className="h-8 w-8 text-blue-600" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 tracking-tight">AI Mock Interviewer</h1>
          <p className="text-lg text-gray-600 max-w-lg mx-auto">
            Upload your resume to generate a custom technical interview.
          </p>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
          {!resume ? (
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-blue-500 hover:bg-blue-50 transition-colors group cursor-pointer relative">
              <input 
                type="file" 
                accept=".pdf"
                onChange={handleUpload}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                disabled={loading}
              />
              <div className="flex flex-col items-center space-y-4">
                {loading ? (
                  <Loader2 className="h-12 w-12 text-blue-500 animate-spin" />
                ) : (
                  <Upload className="h-12 w-12 text-gray-400 group-hover:text-blue-500 transition-colors" />
                )}
                <p className="text-lg font-medium text-gray-900">
                  {loading ? "Parsing Resume..." : "Drop Resume PDF here"}
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-6 text-center">
              <div className="bg-green-50 text-green-700 p-4 rounded-lg flex items-center justify-center gap-2">
                <FileText className="h-5 w-5" />
                <span className="font-medium">{resume.filename}</span>
              </div>
              <p className="text-gray-600 text-sm">
                 Parsed {resume.extracted_text_preview.length} characters of text.
              </p>
              <button 
                onClick={handleStartInterview}
                disabled={starting}
                className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-lg flex items-center justify-center gap-2 transition-all disabled:opacity-70"
              >
                {starting ? (
                    <>
                        <Loader2 className="animate-spin h-5 w-5" />
                        Generating Questions...
                    </>
                ) : (
                    <>
                        Start Interview <ArrowRight className="h-5 w-5" />
                    </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};