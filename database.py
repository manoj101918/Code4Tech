from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database URL
DATABASE_URL = "sqlite:///./resume_evaluation.db"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    student_email = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    parsed_data = Column(Text)  # JSON string of parsed resume data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="resume")

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    location = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    parsed_data = Column(Text)  # JSON string of parsed JD data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="job_description")

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    relevance_score = Column(Float, nullable=False)
    verdict = Column(String, nullable=False)  # High/Medium/Low
    missing_skills = Column(Text)  # JSON string of missing skills
    suggestions = Column(Text)  # JSON string of suggestions
    evaluation_data = Column(Text)  # JSON string of full evaluation data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="evaluations")
    job_description = relationship("JobDescription", back_populates="evaluations")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
