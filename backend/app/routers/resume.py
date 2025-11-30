# File: backend/app/routers/resume.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import tables
from app.services.parser import ResumeParser
import shutil
import os
import uuid

router = APIRouter()
parser = ResumeParser()

# Create 'uploads' folder if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-resume")
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate File Type (Fix: Check if filename exists first)
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Generate unique filename to prevent overwrites
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = f"{UPLOAD_DIR}/{unique_filename}"

    # Save File Locally
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract Text
    text_content = parser.extract_text(file_location)

    if not text_content:
        # Clean up if parsing fails
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail="Failed to parse PDF. The file might be encrypted or empty.")

    # Save to Database
    new_resume = tables.Resume(
        user_id=1, 
        filename=file.filename,
        file_path=file_location,
        extracted_text=text_content
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "id": new_resume.id,
        "filename": new_resume.filename,
        "extracted_text_preview": text_content[:200] + "..." 
    }