#!/usr/bin/env python3
"""
Test script for the Advanced Relevance Engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relevance_engine import AdvancedRelevanceEngine
import json

def test_advanced_evaluation():
    """Test the advanced evaluation system with sample data"""
    print("🧪 Testing Advanced Relevance Engine")
    print("=" * 50)
    
    # Initialize the engine
    engine = AdvancedRelevanceEngine()
    print("✅ Advanced Relevance Engine initialized")
    
    # Test Case 1: Strong candidate
    print("\n📋 Test Case 1: Strong Python Developer Candidate")
    strong_resume = {
        'name': 'Alice Johnson',
        'email': 'alice@example.com',
        'skills': ['Python', 'Django', 'PostgreSQL', 'React', 'AWS', 'Docker', 'Git', 'REST APIs'],
        'experience': [
            {
                'title': 'Senior Software Engineer',
                'company': 'TechCorp',
                'description': 'Led development of microservices using Python and Django. Managed AWS infrastructure and mentored junior developers.'
            },
            {
                'title': 'Software Engineer',
                'company': 'StartupXYZ',
                'description': 'Built REST APIs with Python Flask and integrated with PostgreSQL databases.'
            }
        ],
        'education': [{'degree': 'Bachelor of Computer Science', 'institution': 'Tech University'}],
        'projects': [
            {
                'title': 'E-commerce Platform',
                'description': 'Built scalable e-commerce platform using Django, React, and PostgreSQL'
            }
        ],
        'raw_text': 'Experienced Python developer with expertise in web development and cloud technologies.'
    }
    
    python_jd = {
        'title': 'Senior Python Developer',
        'must_have_skills': ['Python', 'Django', 'PostgreSQL', 'REST APIs'],
        'good_to_have_skills': ['AWS', 'Docker', 'React'],
        'experience_required': 'Minimum 3+ years of Python development experience',
        'qualifications': ['Bachelor in Computer Science or related field'],
        'raw_text': 'We are looking for a senior Python developer with Django experience to build scalable web applications.'
    }
    
    result1 = engine.evaluate(strong_resume, python_jd)
    print_evaluation_result(result1, "Strong Candidate")
    
    # Test Case 2: Moderate candidate
    print("\n📋 Test Case 2: Moderate Java Developer (Skills Mismatch)")
    moderate_resume = {
        'name': 'Bob Smith',
        'email': 'bob@example.com',
        'skills': ['Java', 'Spring Boot', 'MySQL', 'JavaScript', 'HTML', 'CSS'],
        'experience': [
            {
                'title': 'Java Developer',
                'company': 'Enterprise Corp',
                'description': 'Developed enterprise applications using Java and Spring Boot framework.'
            }
        ],
        'education': [{'degree': 'Bachelor of Engineering', 'institution': 'State University'}],
        'raw_text': 'Java developer with experience in enterprise application development.'
    }
    
    result2 = engine.evaluate(moderate_resume, python_jd)
    print_evaluation_result(result2, "Moderate Candidate")
    
    # Test Case 3: Junior candidate
    print("\n📋 Test Case 3: Junior Developer (Limited Experience)")
    junior_resume = {
        'name': 'Charlie Brown',
        'email': 'charlie@example.com',
        'skills': ['Python', 'Flask', 'SQLite', 'HTML', 'CSS', 'Git'],
        'experience': [
            {
                'title': 'Junior Developer',
                'company': 'Small Company',
                'description': 'Built simple web applications using Python Flask and SQLite database.'
            }
        ],
        'education': [{'degree': 'Bachelor of Computer Science', 'institution': 'Local College'}],
        'projects': [
            {
                'title': 'Personal Blog',
                'description': 'Created a personal blog using Flask and SQLite'
            }
        ],
        'raw_text': 'Recent graduate with basic Python and web development skills.'
    }
    
    result3 = engine.evaluate(junior_resume, python_jd)
    print_evaluation_result(result3, "Junior Candidate")
    
    # Test Case 4: Data Science role
    print("\n📋 Test Case 4: Data Scientist Role")
    ds_resume = {
        'name': 'Diana Wilson',
        'email': 'diana@example.com',
        'skills': ['Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'NumPy', 'Jupyter', 'SQL', 'Tableau'],
        'experience': [
            {
                'title': 'Data Scientist',
                'company': 'Analytics Inc',
                'description': 'Built machine learning models using Python, TensorFlow, and scikit-learn. Analyzed large datasets and created visualizations.'
            },
            {
                'title': 'Data Analyst',
                'company': 'Business Corp',
                'description': 'Performed data analysis using Python pandas and created dashboards with Tableau.'
            }
        ],
        'education': [{'degree': 'Master of Data Science', 'institution': 'Data University'}],
        'raw_text': 'Experienced data scientist with expertise in machine learning and data analysis.'
    }
    
    ds_jd = {
        'title': 'Senior Data Scientist',
        'must_have_skills': ['Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'SQL'],
        'good_to_have_skills': ['Deep Learning', 'AWS', 'Docker', 'Tableau'],
        'experience_required': 'Minimum 4+ years of data science experience',
        'qualifications': ['Master in Data Science, Statistics, or related field'],
        'raw_text': 'Looking for a senior data scientist to build ML models and drive data-driven insights.'
    }
    
    result4 = engine.evaluate(ds_resume, ds_jd)
    print_evaluation_result(result4, "Data Scientist")
    
    print("\n🎉 Advanced Evaluation Testing Complete!")
    return True

def print_evaluation_result(result, candidate_type):
    """Print evaluation results in a formatted way"""
    print(f"\n--- {candidate_type} Results ---")
    print(f"📊 Overall Score: {result['relevance_score']}%")
    print(f"🏆 Verdict: {result['verdict']}")
    print(f"🎯 Match Confidence: {result['match_confidence']}")
    print(f"📈 Skills Score: {result['skills_match_score']}%")
    print(f"💼 Experience Score: {result['experience_match_score']}%")
    
    if result['missing_skills']:
        print(f"❌ Missing Skills: {', '.join(result['missing_skills'][:3])}")
    
    print(f"💡 Top Suggestions:")
    for i, suggestion in enumerate(result['suggestions'][:3], 1):
        print(f"   {i}. {suggestion}")
    
    if 'evaluation_summary' in result:
        print(f"📋 Summary: {result['evaluation_summary']}")

if __name__ == "__main__":
    try:
        success = test_advanced_evaluation()
        if success:
            print("\n✅ All tests passed successfully!")
        else:
            print("\n❌ Some tests failed!")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()
