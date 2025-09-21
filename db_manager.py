#!/usr/bin/env python3
"""
Database Management Tool for Resume Evaluation System
"""

import sqlite3
import json
from datetime import datetime
from database import DATABASE_URL, Resume, JobDescription, Evaluation
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Create engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Get database session"""
    return SessionLocal()

def show_database_stats():
    """Show database statistics"""
    db = get_db_session()
    
    try:
        # Count records
        resume_count = db.query(Resume).count()
        jd_count = db.query(JobDescription).count()
        eval_count = db.query(Evaluation).count()
        
        print("=" * 50)
        print("📊 DATABASE STATISTICS")
        print("=" * 50)
        print(f"📄 Resumes: {resume_count}")
        print(f"💼 Job Descriptions: {jd_count}")
        print(f"📊 Evaluations: {eval_count}")
        print("=" * 50)
        
        return {
            'resumes': resume_count,
            'job_descriptions': jd_count,
            'evaluations': eval_count
        }
    finally:
        db.close()

def list_resumes():
    """List all resumes"""
    db = get_db_session()
    
    try:
        resumes = db.query(Resume).all()
        print("\n📄 RESUMES:")
        print("-" * 30)
        
        if not resumes:
            print("No resumes found.")
            return
        
        for resume in resumes:
            print(f"ID: {resume.id}")
            print(f"Name: {resume.student_name}")
            print(f"Email: {resume.student_email}")
            print(f"File: {resume.file_path}")
            print(f"Created: {resume.created_at}")
            print("-" * 30)
            
    finally:
        db.close()

def list_job_descriptions():
    """List all job descriptions"""
    db = get_db_session()
    
    try:
        jds = db.query(JobDescription).all()
        print("\n💼 JOB DESCRIPTIONS:")
        print("-" * 30)
        
        if not jds:
            print("No job descriptions found.")
            return
        
        for jd in jds:
            print(f"ID: {jd.id}")
            print(f"Title: {jd.title}")
            print(f"Location: {jd.location}")
            print(f"File: {jd.file_path}")
            print(f"Created: {jd.created_at}")
            print("-" * 30)
            
    finally:
        db.close()

def list_evaluations():
    """List all evaluations"""
    db = get_db_session()
    
    try:
        evaluations = db.query(Evaluation).all()
        print("\n📊 EVALUATIONS:")
        print("-" * 50)
        
        if not evaluations:
            print("No evaluations found.")
            return
        
        for eval in evaluations:
            print(f"ID: {eval.id}")
            print(f"Resume ID: {eval.resume_id}")
            print(f"JD ID: {eval.job_description_id}")
            print(f"Score: {eval.relevance_score}")
            print(f"Verdict: {eval.verdict}")
            print(f"Created: {eval.created_at}")
            print("-" * 50)
            
    finally:
        db.close()

def show_evaluation_details(eval_id):
    """Show detailed evaluation results"""
    db = get_db_session()
    
    try:
        evaluation = db.query(Evaluation).filter(Evaluation.id == eval_id).first()
        
        if not evaluation:
            print(f"Evaluation with ID {eval_id} not found.")
            return
        
        print(f"\n📊 EVALUATION DETAILS (ID: {eval_id})")
        print("=" * 60)
        print(f"Resume ID: {evaluation.resume_id}")
        print(f"Job Description ID: {evaluation.job_description_id}")
        print(f"Relevance Score: {evaluation.relevance_score}")
        print(f"Verdict: {evaluation.verdict}")
        
        if evaluation.missing_skills:
            missing_skills = json.loads(evaluation.missing_skills)
            print(f"Missing Skills: {missing_skills}")
        
        if evaluation.suggestions:
            suggestions = json.loads(evaluation.suggestions)
            print(f"Suggestions: {suggestions}")
        
        if evaluation.evaluation_data:
            eval_data = json.loads(evaluation.evaluation_data)
            print(f"Detailed Analysis: {json.dumps(eval_data, indent=2)}")
        
        print(f"Created: {evaluation.created_at}")
        print("=" * 60)
        
    finally:
        db.close()

def delete_evaluation(eval_id):
    """Delete an evaluation"""
    db = get_db_session()
    
    try:
        evaluation = db.query(Evaluation).filter(Evaluation.id == eval_id).first()
        
        if not evaluation:
            print(f"Evaluation with ID {eval_id} not found.")
            return
        
        db.delete(evaluation)
        db.commit()
        print(f"✅ Evaluation {eval_id} deleted successfully.")
        
    except Exception as e:
        print(f"❌ Error deleting evaluation: {e}")
        db.rollback()
    finally:
        db.close()

def delete_resume(resume_id):
    """Delete a resume and its evaluations"""
    db = get_db_session()
    
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        
        if not resume:
            print(f"Resume with ID {resume_id} not found.")
            return
        
        # Delete associated evaluations first
        evaluations = db.query(Evaluation).filter(Evaluation.resume_id == resume_id).all()
        for eval in evaluations:
            db.delete(eval)
        
        db.delete(resume)
        db.commit()
        print(f"✅ Resume {resume_id} and {len(evaluations)} associated evaluations deleted successfully.")
        
    except Exception as e:
        print(f"❌ Error deleting resume: {e}")
        db.rollback()
    finally:
        db.close()

def export_data():
    """Export all data to JSON"""
    db = get_db_session()
    
    try:
        data = {
            'resumes': [],
            'job_descriptions': [],
            'evaluations': []
        }
        
        # Export resumes
        resumes = db.query(Resume).all()
        for resume in resumes:
            data['resumes'].append({
                'id': resume.id,
                'student_name': resume.student_name,
                'student_email': resume.student_email,
                'file_path': resume.file_path,
                'created_at': resume.created_at.isoformat(),
                'parsed_data': json.loads(resume.parsed_data) if resume.parsed_data else None
            })
        
        # Export job descriptions
        jds = db.query(JobDescription).all()
        for jd in jds:
            data['job_descriptions'].append({
                'id': jd.id,
                'title': jd.title,
                'location': jd.location,
                'file_path': jd.file_path,
                'created_at': jd.created_at.isoformat(),
                'parsed_data': json.loads(jd.parsed_data) if jd.parsed_data else None
            })
        
        # Export evaluations
        evaluations = db.query(Evaluation).all()
        for eval in evaluations:
            data['evaluations'].append({
                'id': eval.id,
                'resume_id': eval.resume_id,
                'job_description_id': eval.job_description_id,
                'relevance_score': eval.relevance_score,
                'verdict': eval.verdict,
                'missing_skills': json.loads(eval.missing_skills) if eval.missing_skills else None,
                'suggestions': json.loads(eval.suggestions) if eval.suggestions else None,
                'evaluation_data': json.loads(eval.evaluation_data) if eval.evaluation_data else None,
                'created_at': eval.created_at.isoformat()
            })
        
        # Save to file
        filename = f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data exported to {filename}")
        print(f"📊 Exported: {len(data['resumes'])} resumes, {len(data['job_descriptions'])} JDs, {len(data['evaluations'])} evaluations")
        
    finally:
        db.close()

def main():
    """Main menu"""
    while True:
        print("\n" + "=" * 60)
        print("🗄️  DATABASE MANAGEMENT TOOL")
        print("=" * 60)
        print("1. Show Database Statistics")
        print("2. List Resumes")
        print("3. List Job Descriptions")
        print("4. List Evaluations")
        print("5. Show Evaluation Details")
        print("6. Delete Evaluation")
        print("7. Delete Resume")
        print("8. Export All Data")
        print("9. Exit")
        print("=" * 60)
        
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == '1':
            show_database_stats()
        elif choice == '2':
            list_resumes()
        elif choice == '3':
            list_job_descriptions()
        elif choice == '4':
            list_evaluations()
        elif choice == '5':
            eval_id = input("Enter evaluation ID: ").strip()
            try:
                show_evaluation_details(int(eval_id))
            except ValueError:
                print("❌ Invalid evaluation ID")
        elif choice == '6':
            eval_id = input("Enter evaluation ID to delete: ").strip()
            try:
                confirm = input(f"Are you sure you want to delete evaluation {eval_id}? (y/N): ").strip().lower()
                if confirm == 'y':
                    delete_evaluation(int(eval_id))
                else:
                    print("❌ Deletion cancelled")
            except ValueError:
                print("❌ Invalid evaluation ID")
        elif choice == '7':
            resume_id = input("Enter resume ID to delete: ").strip()
            try:
                confirm = input(f"Are you sure you want to delete resume {resume_id} and all its evaluations? (y/N): ").strip().lower()
                if confirm == 'y':
                    delete_resume(int(resume_id))
                else:
                    print("❌ Deletion cancelled")
            except ValueError:
                print("❌ Invalid resume ID")
        elif choice == '8':
            export_data()
        elif choice == '9':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
