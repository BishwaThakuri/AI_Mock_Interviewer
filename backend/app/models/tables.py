from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resumes = relationship("Resume", back_populates="owner")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    file_path = Column(String)  # Local path where PDF is saved
    extracted_text = Column(Text)  # The raw text from PyMuPDF
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="resumes")
    interviews = relationship("InterviewSession", back_populates="resume")

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    interview_goal = Column(String) # e.g. "React Developer Role"
    status = Column(String, default="active") # active, completed
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="interviews")
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    sender = Column(String)
    message_text = Column(Text)
    audio_url = Column(String, nullable=True) # Path to recording
    score = Column(Integer, nullable=True) # 1-10 (If AI graded it)
    feedback = Column(Text, nullable=True) # AI tips
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="messages")