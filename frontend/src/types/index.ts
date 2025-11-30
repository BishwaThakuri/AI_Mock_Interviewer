// What we get back after uploading a PDF
export interface Resume {
  id: number;
  filename: string;
  extracted_text_preview: string;
}

// What we get when starting an interview
export interface InterviewSession {
  session_id: number;
  questions: string[]; // List of strings from Llama 3
}

// What we get after speaking an answer
export interface AnswerResponse {
  transcription: string;
  score: number;
  feedback: string;
}

// For our Chat UI state (Frontend only)
export interface ChatMessage {
  id: string;
  sender: 'ai' | 'user';
  text: string;
  score?: number;
  feedback?: string;
  isAudio?: boolean; // To know if we should show an audio player (optional later)
}