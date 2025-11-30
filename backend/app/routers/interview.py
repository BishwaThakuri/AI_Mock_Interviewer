from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import tables
from app.services.llm import generate_questions

router = APIRouter()

@router.post("/start/{resume_id}")
def start_interview(resume_id: int, db: Session = Depends(get_db)):
    # Get the resume from DB
    resume = db.query(tables.Resume).filter(tables.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Generate Questions using AI
    questions = generate_questions(resume.extracted_text, "Full Stack Developer")
    
    # Save Session to DB
    new_session = tables.InterviewSession(
        resume_id=resume.id,
        interview_goal="Full Stack Developer",
        status="active"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # Save the generated questions as the first "AI Message" context (Invisible to user)
    
    return {
        "session_id": new_session.id,
        "questions": questions
    }