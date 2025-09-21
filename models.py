from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ResumeData(BaseModel):
    """Parsed resume data structure"""
    name: str
    email: str
    phone: Optional[str] = None
    skills: List[str] = []
    education: List[Dict[str, Any]] = []
    experience: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    certifications: List[str] = []
    summary: Optional[str] = None
    raw_text: str

class JobDescriptionData(BaseModel):
    """Parsed job description data structure"""
    title: str
    company: Optional[str] = None
    location: str
    must_have_skills: List[str] = []
    good_to_have_skills: List[str] = []
    qualifications: List[str] = []
    experience_required: Optional[str] = None
    job_type: Optional[str] = None
    description: str
    raw_text: str

class EvaluationResult(BaseModel):
    """Evaluation result structure"""
    relevance_score: float
    verdict: str  # High/Medium/Low
    missing_skills: List[str]
    suggestions: List[str]
    hard_match_score: float
    semantic_match_score: float
    detailed_analysis: Dict[str, Any]

class ResumeUpload(BaseModel):
    student_name: str
    student_email: str

class JobDescriptionUpload(BaseModel):
    title: str
    location: str

class EvaluationRequest(BaseModel):
    resume_id: int
    job_description_id: int
