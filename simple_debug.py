#!/usr/bin/env python3
"""
Simple debug script to isolate the evaluation issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relevance_engine import AdvancedRelevanceEngine

def simple_debug():
    print("🔍 Simple Debug Test")
    print("=" * 30)
    
    engine = AdvancedRelevanceEngine()
    
    # Very simple test data
    resume = {
        'skills': ['Python', 'Django'],
        'experience': [{'title': 'Developer', 'description': 'Python work'}],
        'education': [{'degree': 'Bachelor'}]
    }
    
    jd = {
        'must_have_skills': ['Python'],
        'good_to_have_skills': ['Django'],
        'experience_required': '2 years',
        'qualifications': ['Bachelor']
    }
    
    print("Resume skills:", resume['skills'])
    print("Required skills:", jd['must_have_skills'])
    
    # Test skill normalization
    print("\n--- Testing Skill Normalization ---")
    for skill in resume['skills']:
        normalized = engine.normalize_skill(skill)
        print(f"'{skill}' -> '{normalized}'")
    
    # Test skill matching
    print("\n--- Testing Skills Matching ---")
    try:
        skills_score, skills_details = engine.advanced_skill_matching(resume, jd)
        print(f"Skills score: {skills_score}")
        print(f"Skills details keys: {list(skills_details.keys())}")
        print(f"Matched skills: {skills_details.get('matched_skills', [])}")
        print(f"Missing skills: {skills_details.get('missing_skills', [])}")
    except Exception as e:
        print(f"Error in skills matching: {e}")
        import traceback
        traceback.print_exc()
    
    # Test full evaluation
    print("\n--- Testing Full Evaluation ---")
    try:
        result = engine.evaluate(resume, jd)
        print(f"Final score: {result.get('relevance_score', 'ERROR')}")
        print(f"Verdict: {result.get('verdict', 'ERROR')}")
    except Exception as e:
        print(f"Error in full evaluation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_debug()
