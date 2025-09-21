#!/usr/bin/env python3
"""
Debug script to test the evaluation system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relevance_engine import AdvancedRelevanceEngine
import json

def debug_evaluation():
    print("🔍 Debugging Evaluation System")
    print("=" * 50)
    
    # Initialize the engine
    engine = AdvancedRelevanceEngine()
    print("✅ Engine initialized")
    
    # Simple test data
    resume_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'skills': ['Python', 'Django', 'PostgreSQL', 'React'],
        'experience': [
            {
                'title': 'Senior Software Engineer',
                'company': 'TechCorp',
                'description': 'Developed web applications using Python and Django framework. Worked with PostgreSQL databases.'
            }
        ],
        'education': [{'degree': 'Bachelor of Computer Science', 'institution': 'Tech University'}],
        'raw_text': 'Experienced Python developer with Django and PostgreSQL skills.'
    }
    
    jd_data = {
        'title': 'Python Developer',
        'must_have_skills': ['Python', 'Django', 'PostgreSQL'],
        'good_to_have_skills': ['React', 'AWS'],
        'experience_required': '3+ years of Python development',
        'qualifications': ['Bachelor in Computer Science'],
        'raw_text': 'Looking for a Python developer with Django experience.'
    }
    
    print("\n📋 Test Data:")
    print(f"Resume Skills: {resume_data['skills']}")
    print(f"Required Skills: {jd_data['must_have_skills']}")
    
    print("\n🧪 Running evaluation...")
    
    try:
        # Test individual components
        print("\n--- Testing Skills Matching ---")
        skills_score, skills_details = engine.advanced_skill_matching(resume_data, jd_data)
        print(f"Skills Score: {skills_score:.2f} ({skills_score*100:.1f}%)")
        print(f"Skills Details: {json.dumps(skills_details, indent=2)}")
        
        print("\n--- Testing Experience Evaluation ---")
        exp_score, exp_details = engine.advanced_experience_evaluation(resume_data, jd_data)
        print(f"Experience Score: {exp_score:.2f} ({exp_score*100:.1f}%)")
        print(f"Experience Details: {json.dumps(exp_details, indent=2)}")
        
        print("\n--- Testing Full Evaluation ---")
        result = engine.evaluate(resume_data, jd_data)
        
        print(f"\n🎯 FINAL RESULTS:")
        print(f"Overall Score: {result['relevance_score']}%")
        print(f"Verdict: {result['verdict']}")
        print(f"Match Confidence: {result.get('match_confidence', 'N/A')}")
        print(f"Skills Score: {result.get('skills_match_score', 'N/A')}%")
        print(f"Experience Score: {result.get('experience_match_score', 'N/A')}%")
        print(f"Missing Skills: {result.get('missing_skills', [])}")
        print(f"Suggestions: {len(result.get('suggestions', []))} suggestions")
        
        if result.get('evaluation_summary'):
            print(f"Summary: {result['evaluation_summary']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_evaluation()
    if success:
        print("\n✅ Debug completed successfully!")
    else:
        print("\n❌ Debug failed!")
