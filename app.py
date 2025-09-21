from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime
import json

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = "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"

from database import get_db, init_db, Resume, JobDescription, Evaluation
from resume_parser import ResumeParser
from jd_parser import JobDescriptionParser
from relevance_engine import AdvancedRelevanceEngine
from utils import create_upload_dir

app = FastAPI(title="Automated Resume Relevance Check System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize database
init_db()

# Create upload directories
create_upload_dir()

# Initialize parsers and engine
resume_parser = ResumeParser()
jd_parser = JobDescriptionParser()
relevance_engine = AdvancedRelevanceEngine()

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": {}})

@app.post("/upload/job-description")
async def upload_job_description(
    file: UploadFile = File(...),
    title: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and parse job description"""
    try:
        print(f"Received JD upload: {file.filename}, title: {title}, location: {location}")
        
        # Save uploaded file
        file_path = f"uploads/jd/{file.filename}"
        print(f"Saving file to: {file_path}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"File saved successfully. File size: {os.path.getsize(file_path)} bytes")
        
        # Parse job description
        print("Parsing job description...")
        jd_data = jd_parser.parse(file_path)
        print(f"Parsed data: {jd_data}")
        
        # Save to database
        jd = JobDescription(
            title=title,
            location=location,
            file_path=file_path,
            parsed_data=json.dumps(jd_data),  # Convert to JSON string
            created_at=datetime.now()
        )
        db.add(jd)
        db.commit()
        db.refresh(jd)
        
        print(f"Job description saved to database with ID: {jd.id}")
        return {"message": "Job description uploaded successfully", "jd_id": jd.id}
    except Exception as e:
        print(f"Error in JD upload: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload/resume")
async def upload_resume(
    file: UploadFile = File(...),
    student_name: str = Form(...),
    student_email: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and parse resume"""
    try:
        print(f"Received resume upload: {file.filename}, name: {student_name}, email: {student_email}")
        
        # Save uploaded file
        file_path = f"uploads/resumes/{file.filename}"
        print(f"Saving file to: {file_path}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"File saved successfully. File size: {os.path.getsize(file_path)} bytes")
        
        # Parse resume
        print("Parsing resume...")
        resume_data = resume_parser.parse(file_path)
        print(f"Parsed data: {resume_data}")
        
        # Save to database
        resume = Resume(
            student_name=student_name,
            student_email=student_email,
            file_path=file_path,
            parsed_data=json.dumps(resume_data),  # Convert to JSON string
            created_at=datetime.now()
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        print(f"Resume saved to database with ID: {resume.id}")
        return {"message": "Resume uploaded successfully", "resume_id": resume.id}
    except Exception as e:
        print(f"Error in resume upload: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/evaluate/{resume_id}/{jd_id}")
async def evaluate_resume(
    resume_id: int,
    jd_id: int,
    db: Session = Depends(get_db)
):
    """Evaluate resume against job description"""
    try:
        print(f"Starting evaluation for resume {resume_id} and JD {jd_id}")
        
        # Get resume and job description
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
        
        if not resume or not jd:
            raise HTTPException(status_code=404, detail="Resume or Job Description not found")
        
        print(f"Resume data type: {type(resume.parsed_data)}")
        print(f"JD data type: {type(jd.parsed_data)}")
        
        # Parse JSON strings back to dictionaries
        resume_data = json.loads(resume.parsed_data) if isinstance(resume.parsed_data, str) else resume.parsed_data
        jd_data = json.loads(jd.parsed_data) if isinstance(jd.parsed_data, str) else jd.parsed_data
        
        print(f"Parsed resume data: {resume_data}")
        print(f"Parsed JD data: {jd_data}")
        
        # Run evaluation
        evaluation_result = relevance_engine.evaluate(resume_data, jd_data)
        print(f"Evaluation result: {evaluation_result}")
        
        # Save evaluation
        evaluation = Evaluation(
            resume_id=resume_id,
            job_description_id=jd_id,
            relevance_score=evaluation_result["relevance_score"],
            verdict=evaluation_result["verdict"],
            missing_skills=json.dumps(evaluation_result["missing_skills"]),  # Convert to JSON string
            suggestions=json.dumps(evaluation_result["suggestions"]),  # Convert to JSON string
            evaluation_data=json.dumps(evaluation_result),  # Convert to JSON string
            created_at=datetime.now()
        )
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        
        print(f"Evaluation saved with ID: {evaluation.id}")
        return evaluation_result
    except Exception as e:
        print(f"Error in evaluation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/resumes")
async def get_resumes(db: Session = Depends(get_db)):
    """Get all resumes"""
    resumes = db.query(Resume).all()
    return [{"id": r.id, "student_name": r.student_name, "student_email": r.student_email, "created_at": r.created_at} for r in resumes]

@app.get("/job-descriptions")
async def get_job_descriptions(db: Session = Depends(get_db)):
    """Get all job descriptions"""
    jds = db.query(JobDescription).all()
    return [{"id": j.id, "title": j.title, "location": j.location, "created_at": j.created_at} for j in jds]

@app.get("/evaluations")
async def get_evaluations(
    jd_id: Optional[int] = None,
    min_score: Optional[int] = None,
    verdict: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get evaluations with optional filters"""
    query = db.query(Evaluation)
    
    if jd_id:
        query = query.filter(Evaluation.job_description_id == jd_id)
    if min_score:
        query = query.filter(Evaluation.relevance_score >= min_score)
    if verdict:
        query = query.filter(Evaluation.verdict == verdict)
    
    evaluations = query.all()
    return [
        {
            "id": e.id,
            "resume_id": e.resume_id,
            "job_description_id": e.job_description_id,
            "relevance_score": e.relevance_score,
            "verdict": e.verdict,
            "missing_skills": e.missing_skills,
            "suggestions": e.suggestions,
            "created_at": e.created_at
        } for e in evaluations
    ]

@app.get("/evaluation/{evaluation_id}")
async def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    """Get detailed evaluation"""
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    resume = db.query(Resume).filter(Resume.id == evaluation.resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == evaluation.job_description_id).first()
    
    return {
        "evaluation": {
            "id": evaluation.id,
            "relevance_score": evaluation.relevance_score,
            "verdict": evaluation.verdict,
            "missing_skills": evaluation.missing_skills,
            "suggestions": evaluation.suggestions,
            "evaluation_data": evaluation.evaluation_data,
            "created_at": evaluation.created_at
        },
        "resume": {
            "id": resume.id,
            "student_name": resume.student_name,
            "student_email": resume.student_email
        },
        "job_description": {
            "id": jd.id,
            "title": jd.title,
            "location": jd.location
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
