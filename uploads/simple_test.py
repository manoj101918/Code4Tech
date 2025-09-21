#!/usr/bin/env python3
"""
Simple test for the Advanced Relevance Engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from relevance_engine import AdvancedRelevanceEngine
    print("✅ Successfully imported AdvancedRelevanceEngine")
    
    # Initialize the engine
    engine = AdvancedRelevanceEngine()
    print("✅ Engine initialized successfully")
    
    # Simple test data
    resume = {
        'skills': ['Python', 'Django', 'PostgreSQL'],
        'experience': [{'title': 'Developer', 'company': 'TechCorp', 'description': 'Python development'}],
        'education': [{'degree': 'Bachelor CS'}]
    }
    
    jd = {
        'title': 'Python Developer',
        'must_have_skills': ['Python', 'Django'],
        'good_to_have_skills': ['PostgreSQL'],
        'experience_required': '2+ years',
        'qualifications': ['Bachelor']
    }
    
    print("🧪 Running evaluation...")
    result = engine.evaluate(resume, jd)
    
    print(f"📊 Score: {result['relevance_score']}%")
    print(f"🏆 Verdict: {result['verdict']}")
    print(f"🎯 Confidence: {result['match_confidence']}")
    print("✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
