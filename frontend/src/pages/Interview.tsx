import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useParams, useNavigate } from 'react-router-dom';
import { Mic, Square, Send, Bot, Loader2, Home } from 'lucide-react';
import { api } from '../api/client';
import { useAudioRecorder } from '../hooks/useAudioRecorder';
import type { ChatMessage } from '../types';

export const Interview = () => {
  const { sessionId } = useParams();
  const location = useLocation();
  const navigate = useNavigate(); 
  const initialQuestions = location.state?.questions || [];
  
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [processing, setProcessing] = useState(false);
  const [isFinished, setIsFinished] = useState(false);
  
  const { isRecording, startRecording, stopRecording, audioBlob, setAudioBlob } = useAudioRecorder();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize Chat
  useEffect(() => {
    if (initialQuestions.length > 0 && messages.length === 0) {
      setMessages([
        {
          id: 'init-1',
          sender: 'ai',
          text: `Hello! I've reviewed your resume. Let's start with your first technical question:\n\n${initialQuestions[0]}`
        }
      ]);
    }
  }, [initialQuestions]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle Audio Submission
  const handleSubmitAnswer = async () => {
    if (!audioBlob || !sessionId) return;

    const currentQuestion = initialQuestions[currentQuestionIndex];
    setProcessing(true);

    const userMsgId = Date.now().toString();
    setMessages(prev => [...prev, { id: userMsgId, sender: 'user', text: "🎤 Audio Answer Submitted...", isAudio: true }]);

    try {
      const response = await api.submitAnswer(Number(sessionId), currentQuestion, audioBlob);

      setMessages(prev => prev.map(msg => 
        msg.id === userMsgId 
          ? { ...msg, text: response.transcription, score: response.score, feedback: response.feedback }
          : msg
      ));

      if (currentQuestionIndex < initialQuestions.length - 1) {
        const nextQ = initialQuestions[currentQuestionIndex + 1];
        setCurrentQuestionIndex(prev => prev + 1);
        
        setTimeout(() => {
          setMessages(prev => [...prev, {
            id: Date.now().toString(),
            sender: 'ai',
            text: `Good. Let's move on:\n\n${nextQ}`
          }]);
        }, 1000);
      } else {
        // --- INTERVIEW FINISHED LOGIC ---
        setTimeout(() => {
          setMessages(prev => [...prev, {
            id: 'end',
            sender: 'ai',
            text: "That concludes our interview! Great job. Check your scores above."
          }]);
          setIsFinished(true);
        }, 1000);
      }

    } catch (err) {
      console.error(err);
      alert("Error submitting answer. Check backend console.");
    } finally {
      setProcessing(false);
      setAudioBlob(null);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 max-w-4xl mx-auto shadow-2xl overflow-hidden">
      
      {/* Header with Home Button */}
      <div className="bg-white border-b p-4 flex items-center justify-between shadow-sm z-10">
        <div className="flex items-center gap-2">
          <Bot className="text-blue-600 h-6 w-6" />
          <h1 className="font-bold text-xl text-gray-800">AI Interviewer</h1>
        </div>
        
        <div className="flex items-center gap-4">
            <div className="text-sm text-gray-500 hidden sm:block">
            Question {currentQuestionIndex + 1} of {initialQuestions.length}
            </div>
            {/* Home Button */}
            <button 
                onClick={() => navigate('/')}
                className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-all"
                title="Back to Home"
            >
                <Home className="h-6 w-6" />
            </button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-4 shadow-sm ${
              msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-white text-gray-800 border border-gray-200'
            }`}>
              <p className="whitespace-pre-wrap">{msg.text}</p>
              
              {msg.score !== undefined && (
                <div className="mt-3 pt-3 border-t border-blue-400/30">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-bold uppercase opacity-80">AI Feedback</span>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                      msg.score >= 7 ? 'bg-green-400 text-green-900' : 'bg-yellow-400 text-yellow-900'
                    }`}>
                      Score: {msg.score}/10
                    </span>
                  </div>
                  <p className="text-sm opacity-90 italic">{msg.feedback}</p>
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Controls Area */}
      <div className="bg-white border-t p-6">
        <div className="flex flex-col items-center gap-4">
          
          {/* Conditional Rendering: Show Controls OR 'Start New' button */}
          {!isFinished ? (
            <>
                <div className="h-6 text-sm font-medium text-gray-500">
                    {processing ? "AI is thinking..." : isRecording ? "Recording... (Speak now)" : audioBlob ? "Ready to Submit" : "Ready to Record"}
                </div>

                <div className="flex items-center gap-4">
                    {!audioBlob ? (
                    <button
                        onClick={isRecording ? stopRecording : startRecording}
                        className={`p-6 rounded-full transition-all shadow-lg ${
                        isRecording 
                            ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                            : 'bg-blue-600 hover:bg-blue-700'
                        }`}
                    >
                        {isRecording ? <Square className="h-8 w-8 text-white" /> : <Mic className="h-8 w-8 text-white" />}
                    </button>
                    ) : (
                    <div className="flex gap-4">
                        <button 
                        onClick={() => setAudioBlob(null)} 
                        className="px-6 py-3 rounded-full text-gray-600 hover:bg-gray-100 font-medium"
                        >
                        Retry
                        </button>
                        <button
                        onClick={handleSubmitAnswer}
                        disabled={processing}
                        className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white rounded-full font-bold shadow-lg flex items-center gap-2"
                        >
                        {processing ? <Loader2 className="animate-spin" /> : <Send className="h-5 w-5" />}
                        Submit Answer
                        </button>
                    </div>
                    )}
                </div>
            </>
          ) : (
            /* FINISHED STATE */
            <div className="text-center space-y-3">
                <p className="text-green-600 font-medium">Interview Complete!</p>
                <button
                    onClick={() => navigate('/')}
                    className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-lg flex items-center gap-2 transition-transform hover:scale-105"
                >
                    <Home className="h-5 w-5" />
                    Start New Interview
                </button>
            </div>
          )}
          
        </div>
      </div>

    </div>
  );
};