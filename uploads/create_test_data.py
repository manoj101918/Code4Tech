#!/usr/bin/env python3
"""
Create proper test data in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, Resume, JobDescription
import json
from datetime import datetime

def create_test_data():
    print("🔧 Creating Test Data")
    print("=" * 30)
    
    db = next(get_db())
    
    # Create a proper resume
    resume_data = {
        'name': 'Alice Johnson',
        'email': 'alice@example.com',
        'skills': ['Python', 'Django', 'PostgreSQL', 'React', 'AWS', 'Docker'],
        'experience': [
            {
                'title': 'Senior Software Engineer',
                'company': 'TechCorp',
                'description': 'Led development of web applications using Python and Django. Worked with PostgreSQL databases and deployed on AWS.'
            },
            {
                'title': 'Software Engineer',
                'company': 'StartupXYZ',
                'description': 'Built REST APIs with Python Flask. Integrated with PostgreSQL and Redis.'
            }
        ],
        'education': [
            {
                'degree': 'Bachelor of Computer Science',
                'institution': 'Tech University'
            }
        ],
        'projects': [
            {
                'title': 'E-commerce Platform',
                'description': 'Built scalable platform using Django and React'
            }
        ],
        'raw_text': 'Experienced Python developer with Django and PostgreSQL expertise.'
    }
    
    # Create a proper job description
    jd_data = {
        'title': 'Senior Python Developer',
        'must_have_skills': ['Python', 'Django', 'PostgreSQL'],
        'good_to_have_skills': ['React', 'AWS', 'Docker'],
        'experience_required': '3+ years of Python development experience',
        'qualifications': ['Bachelor in Computer Science or related field'],
        'raw_text': 'We are looking for a senior Python developer with Django experience to build scalable web applications.'
    }
    
    try:
        # Add resume
        resume = Resume(
            student_name='Alice Johnson',
            student_email='alice@example.com',
            file_path='test_resume.pdf',
            parsed_data=json.dumps(resume_data),
            created_at=datetime.now()
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        print(f"✅ Created resume with ID: {resume.id}")
        
        # Add job description
        jd = JobDescription(
            title='Senior Python Developer',
            location='San Francisco, CA',
            file_path='test_jd.pdf',
            parsed_data=json.dumps(jd_data),
            created_at=datetime.now()
        )
        db.add(jd)
        db.commit()
        db.refresh(jd)
        print(f"✅ Created job description with ID: {jd.id}")
        
        print(f"\n🧪 Now you can test evaluation with:")
        print(f"Resume ID: {resume.id}")
        print(f"Job Description ID: {jd.id}")
        
        # Test the evaluation directly
        print(f"\n🔍 Testing evaluation...")
        from relevance_engine import AdvancedRelevanceEngine
        engine = AdvancedRelevanceEngine()
        
        result = engine.evaluate(resume_data, jd_data)
        print(f"✅ Evaluation successful!")
        print(f"Score: {result['relevance_score']}%")
        print(f"Verdict: {result['verdict']}")
        print(f"Confidence: {result.get('match_confidence', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
