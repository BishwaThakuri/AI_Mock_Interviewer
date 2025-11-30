from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import tables
from app.services.llm import generate_questions, grade_answer
from app.services.audio import AudioService
import shutil
import os

router = APIRouter()

# Initialize Whisper ONCE (Global variable) to avoid reloading it every request
audio_service = AudioService()

@router.post("/start/{resume_id}")
def start_interview(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(tables.Resume).filter(tables.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    questions = generate_questions(resume.extracted_text, "Full Stack Developer")
    
    new_session = tables.InterviewSession(
        resume_id=resume.id,
        interview_goal="Full Stack Developer",
        status="active"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "session_id": new_session.id,
        "questions": questions
    }

@router.post("/{session_id}/answer")
def submit_answer(
    session_id: int, 
    question: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Save Audio
    session_dir = f"uploads/session_{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    file_location = f"{session_dir}/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Transcribe (DYNAMIC CONTEXT)
    # We pass the 'question' as the context hint. 
    # If question is about Laravel, Whisper listens for Laravel terms.
    user_answer_text = audio_service.transcribe(file_location, context_text=question)
    
    if not user_answer_text:
        raise HTTPException(status_code=400, detail="Could not transcribe audio")
        
    # 3. Grade
    grading = grade_answer(question, user_answer_text)
    
    return {
        "transcription": user_answer_text,
        "score": grading.get("score"),
        "feedback": grading.get("feedback")
    }