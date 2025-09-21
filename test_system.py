#!/usr/bin/env python3
"""
Test script for the Resume Relevance Check System
"""

import os
import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import fitz  # PyMuPDF
        print("✅ PyMuPDF imported successfully")
    except ImportError as e:
        print(f"❌ PyMuPDF import failed: {e}")
        return False
    
    try:
        from docx import Document
        print("✅ python-docx imported successfully")
    except ImportError as e:
        print(f"❌ python-docx import failed: {e}")
        return False
    
    try:
        import spacy
        print("✅ spaCy imported successfully")
    except ImportError as e:
        print(f"❌ spaCy import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ scikit-learn import failed: {e}")
        return False
    
    return True

def test_spacy_model():
    """Test if spaCy model is available"""
    print("\nTesting spaCy model...")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model loaded successfully")
        
        # Test basic functionality
        doc = nlp("This is a test sentence.")
        print(f"✅ Basic NLP processing works: {len(doc)} tokens")
        return True
    except OSError as e:
        print(f"❌ spaCy model not found: {e}")
        print("   Run: python -m spacy download en_core_web_sm")
        return False
    except Exception as e:
        print(f"❌ Error loading spaCy model: {e}")
        return False

def test_database_connection():
    """Test database connection and table creation"""
    print("\nTesting database connection...")
    
    try:
        from database import init_db, get_db
        from sqlalchemy.orm import Session
        
        # Initialize database
        init_db()
        print("✅ Database initialized successfully")
        
        # Test database session
        db = next(get_db())
        print("✅ Database session created successfully")
        db.close()
        
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_parsers():
    """Test resume and JD parsers"""
    print("\nTesting parsers...")
    
    try:
        from resume_parser import ResumeParser
        from jd_parser import JobDescriptionParser
        
        # Test resume parser initialization
        resume_parser = ResumeParser()
        print("✅ Resume parser initialized")
        
        # Test JD parser initialization
        jd_parser = JobDescriptionParser()
        print("✅ Job description parser initialized")
        
        return True
    except Exception as e:
        print(f"❌ Parser initialization failed: {e}")
        return False

def test_relevance_engine():
    """Test relevance engine"""
    print("\nTesting relevance engine...")
    
    try:
        from relevance_engine import RelevanceEngine
        
        # Initialize engine
        engine = RelevanceEngine()
        print("✅ Relevance engine initialized")
        
        # Test with sample data
        sample_resume = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'skills': ['Python', 'JavaScript', 'SQL'],
            'experience': [{'title': 'Software Engineer', 'company': 'Tech Corp'}],
            'education': [{'degree': 'Bachelor of Computer Science'}],
            'raw_text': 'John Doe is a software engineer with Python and JavaScript skills.'
        }
        
        sample_jd = {
            'title': 'Python Developer',
            'must_have_skills': ['Python', 'SQL'],
            'good_to_have_skills': ['JavaScript'],
            'qualifications': ['Bachelor'],
            'raw_text': 'We are looking for a Python developer with SQL experience.'
        }
        
        # Run evaluation
        result = engine.evaluate(sample_resume, sample_jd)
        print(f"✅ Evaluation completed: Score = {result['relevance_score']}%")
        print(f"   Verdict: {result['verdict']}")
        
        return True
    except Exception as e:
        print(f"❌ Relevance engine test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'app.py',
        'database.py',
        'models.py',
        'resume_parser.py',
        'jd_parser.py',
        'relevance_engine.py',
        'utils.py',
        'requirements.txt',
        'templates/dashboard.html',
        'static/js/dashboard.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    return True

def test_openai_integration():
    """Test OpenAI integration (if API key is available)"""
    print("\nTesting OpenAI integration...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set - skipping OpenAI tests")
        return True
    
    try:
        from relevance_engine import RelevanceEngine
        engine = RelevanceEngine()
        
        if engine.embeddings:
            print("✅ OpenAI embeddings available")
        else:
            print("⚠️  OpenAI embeddings not available")
        
        if engine.llm:
            print("✅ OpenAI LLM available")
        else:
            print("⚠️  OpenAI LLM not available")
        
        return True
    except Exception as e:
        print(f"❌ OpenAI integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Resume Relevance Check System")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("spaCy Model", test_spacy_model),
        ("Database", test_database_connection),
        ("Parsers", test_parsers),
        ("Relevance Engine", test_relevance_engine),
        ("OpenAI Integration", test_openai_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("Run 'python run.py' to start the application.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed correctly.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
