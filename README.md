# 🤖 AI Mock Interviewer & Career Coach

**A full-stack, voice-interactive interview platform that acts as a real-time technical recruiter.**

![React](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-blue) ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green) ![AI](https://img.shields.io/badge/AI-Llama%203%20%7C%20Whisper-purple)

## 💡 Overview
This project is an advanced AI Agent designed to help job seekers practice technical interviews. Unlike generic chatbots, this system:
1.  **Parses your actual Resume** (PDF) to understand your tech stack.
2.  **Generates custom questions** based on your specific experience using **Llama 3**.
3.  **Listens to your spoken answers** using local Speech-to-Text (**Faster-Whisper**).
4.  **Grades your response** on technical accuracy and communication clarity.

## 🛠️ Architecture & Tech Stack

### **Frontend (Client)**
* **Framework:** React (Vite) + TypeScript
* **Styling:** Tailwind CSS + Lucide Icons
* **Audio:** Custom `useAudioRecorder` hook (MediaStream API)
* **State:** React Hooks + Axios

### **Backend (Server)**
* **API:** FastAPI (Python)
* **Database:** SQLite + SQLAlchemy (Relational Data Models)
* **PDF Engine:** PyMuPDF (Fitz) for layout-preserving text extraction

### **AI Pipeline (The Brains)**
* **LLM Inference:** Groq Cloud API (Llama-3.3-70b-versatile) for sub-second latency.
* **Speech-to-Text:** `faster-whisper` (running locally on CPU/GPU).
    * *Optimization:* Implemented **Context Injection** to prime the model with the interview question (e.g., distinguishing "Java" from "Jabba").

## ✨ Key Features
* **📄 Intelligent Resume Parsing:** Extracts skills and context from raw PDF binaries.
* **🧠 Context-Aware Questioning:** The AI doesn't ask random questions; it asks about *your* projects (e.g., "Tell me how you optimized Laravel queries in your E-commerce project?").
* **🎙️ Real-Time Voice Processing:** Records audio in the browser, streams to the backend, and transcribes with high accuracy using a fine-tuned prompt strategy.
* **📊 Smart Grading:** Llama 3 evaluates answers with "Phonetic Forgiveness" (understanding that "Sequel" usually means "SQL" in a voice context).

## 🚀 Quick Start Guide

### Prerequisites
* Node.js (v18+)
* Python (v3.9+)
* Groq API Key (Free)

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (FastAPI, Torch, Whisper, etc.)
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env

# Start Server (Auto-downloads Whisper model on first run)
uvicorn app.main:app --reload
```
Backend runs on: `http://127.0.0.1:8000` Swagger Docs: `http://127.0.0.1:8000/docs`

### 2. Frontend Setup
```bash 
cd frontend

# Install dependencies
npm install

# Start React Dev Server
npm run dev
```
Frontend runs on: `http://localhost:5173`

## 🧠 Engineering Decisions
### Why Local Whisper instead of OpenAI API?
    To reduce costs and latency. Running faster-whisper (base model) locally allows for unlimited audio transcription without hitting API rate limits or credit usage.

### Why Groq?
    Real-time chat requires speed. Groq's LPU (Language Processing Unit) inference engine delivers tokens significantly faster than standard GPT-4 endpoints, making the interview feel conversational.

### Why TypeScript?
    The backend returns complex JSON structures (Questions, Grading Feedback, Transcription). TypeScript ensures strict type safety between the API response and the React UI, preventing runtime crashes.

### 🔜 Future Roadmap
- Video Analysis: Use Computer Vision to detect eye contact and posture.
- User Auth: Save interview history for multiple users.
- TTS (Text-to-Speech): Give the AI a voice to speak the questions aloud.

**Built by [Bishwa Thakuri](https://bishwathakuri.com.np/) 🚀 👨‍💻**