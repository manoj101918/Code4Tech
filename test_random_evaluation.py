#!/usr/bin/env python3
"""
Test the random evaluation system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from relevance_engine import AdvancedRelevanceEngine

def test_random_evaluation():
    print("🎲 Testing Random Evaluation System")
    print("=" * 50)
    
    engine = AdvancedRelevanceEngine()
    
    # Simple test data (content doesn't matter for random evaluation)
    resume_data = {
        'skills': ['Python', 'Django'],
        'experience': [{'title': 'Developer'}],
        'education': [{'degree': 'Bachelor'}]
    }
    
    jd_data = {
        'must_have_skills': ['Python'],
        'good_to_have_skills': ['Django']
    }
    
    print("🔄 Running 5 random evaluations for the same candidate:")
    print("-" * 50)
    
    for i in range(1, 6):
        result = engine.evaluate(resume_data, jd_data)
        print(f"Evaluation #{i}:")
        print(f"  📊 Score: {result['relevance_score']}%")
        print(f"  🏆 Verdict: {result['verdict']}")
        print(f"  🎯 Confidence: {result['match_confidence']}")
        print(f"  🔧 Skills: {result['skills_match_score']}%")
        print(f"  💼 Experience: {result['experience_match_score']}%")
        print(f"  ❌ Missing: {len(result['missing_skills'])} skills")
        print(f"  💡 Suggestions: {len(result['suggestions'])} items")
        print()
    
    print("✅ Random evaluation system working!")
    print("\n🔧 To disable random scores and use actual evaluation:")
    print("   engine.enable_random_scores(False)")

if __name__ == "__main__":
    test_random_evaluation()
