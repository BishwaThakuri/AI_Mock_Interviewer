from fastapi import FastAPI
from app.database import engine, Base
from app.routers import resume, interview

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Mock Interviewer")

# Include Routers
app.include_router(resume.router, prefix="/api", tags=["Resume"])
app.include_router(interview.router, prefix="/api", tags=["Interview"])

@app.get("/")
def read_root():
    return {"message": "Database & API are running!"}