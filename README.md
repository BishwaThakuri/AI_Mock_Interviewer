# 🤖 AI Mock Interviewer & Career Coach

A real-time, voice-interactive interview platform that acts as a personal career coach. Users upload their resumes, and the system generates context-aware technical questions, listens to spoken answers, and provides instant AI-driven feedback on clarity, technical accuracy, and confidence.

## 🚀 Features (In Progress)
- **Smart Resume Parsing**: Extracts skills and experience using a custom Python parser (PyMuPDF).
- **Context-Aware Questioning**: Generates unique interview questions based on the candidate's profile using **Llama 3 (via Groq)**.
- **Voice Interaction**: Real-time Speech-to-Text using **Faster-Whisper** (local execution) and browser-native Text-to-Speech.
- **AI Grading**: detailed scoring of answers with actionable feedback.

## 🛠️ Tech Stack

### Frontend
- **Framework**: React (Vite) + TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **Audio**: MediaStream Recording API

### Backend
- **API**: FastAPI (Python)
- **Database**: SQLite (SQLAlchemy)
- **AI/ML**: 
  - **LLM**: Llama 3-8b (Groq API)
  - **Speech-to-Text**: Faster-Whisper (Local)
  - **PDF Processing**: PyMuPDF (Fitz)

## 📂 Project Structure
```bash
/backend    # FastAPI server, Database models, and AI Logic
/frontend   # React application (TypeScript)
```