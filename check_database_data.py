#!/usr/bin/env python3
"""
Check what data is actually in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, Resume, JobDescription
import json

def check_database():
    print("🔍 Checking Database Data")
    print("=" * 30)
    
    db = next(get_db())
    
    # Check resumes
    print("\n📄 RESUMES:")
    resumes = db.query(Resume).all()
    for resume in resumes:
        print(f"ID: {resume.id}, Name: {resume.student_name}")
        print(f"Data type: {type(resume.parsed_data)}")
        
        try:
            if isinstance(resume.parsed_data, str):
                data = json.loads(resume.parsed_data)
            else:
                data = resume.parsed_data
            
            print(f"Skills: {data.get('skills', 'MISSING')}")
            print(f"Experience count: {len(data.get('experience', []))}")
            print(f"Education count: {len(data.get('education', []))}")
            print("---")
        except Exception as e:
            print(f"Error parsing resume data: {e}")
            print(f"Raw data: {str(resume.parsed_data)[:200]}...")
            print("---")
    
    # Check job descriptions
    print("\n💼 JOB DESCRIPTIONS:")
    jds = db.query(JobDescription).all()
    for jd in jds:
        print(f"ID: {jd.id}, Title: {jd.title}")
        print(f"Data type: {type(jd.parsed_data)}")
        
        try:
            if isinstance(jd.parsed_data, str):
                data = json.loads(jd.parsed_data)
            else:
                data = jd.parsed_data
            
            print(f"Must have skills: {data.get('must_have_skills', 'MISSING')}")
            print(f"Good to have skills: {data.get('good_to_have_skills', 'MISSING')}")
            print(f"Experience required: {data.get('experience_required', 'MISSING')}")
            print("---")
        except Exception as e:
            print(f"Error parsing JD data: {e}")
            print(f"Raw data: {str(jd.parsed_data)[:200]}...")
            print("---")
    
    db.close()

if __name__ == "__main__":
    check_database()
