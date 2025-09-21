#!/usr/bin/env python3
"""
Test the actual API response
"""

import requests
import json

def test_api():
    print("🔍 Testing API Response")
    print("=" * 30)
    
    try:
        # Test the evaluation endpoint
        response = requests.post("http://localhost:8000/evaluate/1/1")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n📊 API Response:")
            print(f"Relevance Score: {result.get('relevance_score', 'MISSING')}")
            print(f"Verdict: {result.get('verdict', 'MISSING')}")
            print(f"Match Confidence: {result.get('match_confidence', 'MISSING')}")
            print(f"Skills Score: {result.get('skills_match_score', 'MISSING')}")
            print(f"Experience Score: {result.get('experience_match_score', 'MISSING')}")
            print(f"Missing Skills: {result.get('missing_skills', 'MISSING')}")
            print(f"Suggestions Count: {len(result.get('suggestions', []))}")
            
            # Check if all expected fields are present
            expected_fields = [
                'relevance_score', 'verdict', 'match_confidence', 
                'skills_match_score', 'experience_match_score',
                'missing_skills', 'suggestions', 'evaluation_summary'
            ]
            
            missing_fields = [field for field in expected_fields if field not in result]
            if missing_fields:
                print(f"\n⚠️  Missing fields: {missing_fields}")
            else:
                print(f"\n✅ All expected fields present")
                
            # Print full response for debugging
            print(f"\n🔍 Full Response:")
            print(json.dumps(result, indent=2)[:1000] + "..." if len(str(result)) > 1000 else json.dumps(result, indent=2))
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api()
