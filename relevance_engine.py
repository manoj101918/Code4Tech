import json
import re
from typing import Dict, List, Any, Tuple, Set
from difflib import SequenceMatcher
import openai
import os
import math
from collections import defaultdict
import random

try:
    from config import USE_RANDOM_SCORES, RANDOM_SCORE_RANGES
except ImportError:
    # Fallback if config.py doesn't exist
    USE_RANDOM_SCORES = True
    RANDOM_SCORE_RANGES = {
        'excellent': (85, 95),
        'strong': (75, 84),
        'good': (65, 74),
        'potential': (55, 64),
        'moderate': (45, 54),
        'weak': (30, 44),
        'poor': (15, 29)
    }

class AdvancedRelevanceEngine:
    def __init__(self):
        # Initialize OpenAI (you'll need to set OPENAI_API_KEY environment variable)
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
            print("OpenAI API key set successfully. Using advanced semantic matching.")
        else:
            print("Warning: OPENAI_API_KEY not set. Using advanced rule-based matching.")
            self.openai_client = None
        
        # Advanced skill categorization
        self.skill_categories = {
            'programming_languages': {
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 
                'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl'
            },
            'web_technologies': {
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
                'flask', 'spring', 'laravel', 'bootstrap', 'jquery', 'webpack', 'sass', 'less'
            },
            'databases': {
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
                'oracle', 'sql server', 'sqlite', 'dynamodb', 'neo4j', 'couchdb'
            },
            'cloud_platforms': {
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'kubernetes', 'docker', 'terraform', 'ansible', 'jenkins'
            },
            'data_science': {
                'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
                'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'tableau', 'power bi'
            },
            'mobile_development': {
                'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
                'swift', 'kotlin', 'objective-c'
            },
            'devops': {
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
                'terraform', 'ansible', 'chef', 'puppet', 'nagios', 'prometheus'
            },
            'testing': {
                'unit testing', 'integration testing', 'selenium', 'jest', 'pytest',
                'junit', 'cypress', 'postman', 'jmeter', 'cucumber'
            }
        }
        
        # Skill synonyms and variations
        self.skill_synonyms = {
            'javascript': ['js', 'ecmascript', 'node.js', 'nodejs'],
            'python': ['py', 'python3'],
            'machine learning': ['ml', 'artificial intelligence', 'ai'],
            'deep learning': ['dl', 'neural networks', 'cnn', 'rnn'],
            'react': ['reactjs', 'react.js'],
            'angular': ['angularjs', 'angular.js'],
            'vue': ['vuejs', 'vue.js'],
            'postgresql': ['postgres', 'psql'],
            'mongodb': ['mongo'],
            'aws': ['amazon web services'],
            'gcp': ['google cloud platform'],
            'kubernetes': ['k8s'],
            'docker': ['containerization'],
            'ci/cd': ['continuous integration', 'continuous deployment', 'devops pipeline']
        }
        
        # Experience level indicators
        self.experience_indicators = {
            'senior': ['senior', 'lead', 'principal', 'architect', 'manager', 'director'],
            'mid': ['mid-level', 'intermediate', 'experienced', '3-5 years', '2-4 years'],
            'junior': ['junior', 'entry-level', 'graduate', 'fresher', '0-2 years', 'intern']
        }
        
        # Dynamic scoring weights based on job requirements
        self.base_weights = {
            'skills_match': 0.45,
            'experience_relevance': 0.25,
            'education_match': 0.15,
            'semantic_similarity': 0.15
        }
        
        # Advanced scoring parameters
        self.scoring_params = {
            'critical_skill_multiplier': 2.0,
            'experience_level_bonus': 0.2,
            'domain_expertise_bonus': 0.15,
            'skill_diversity_bonus': 0.1,
            'recency_factor': 0.1
        }
        
        # Stop words for text processing
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'i', 'me', 'my', 'myself', 'we', 'our',
            'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves'
        }
        
        # Randomization settings from config
        self.use_random_scores = USE_RANDOM_SCORES
        self.random_ranges = RANDOM_SCORE_RANGES
    
    def enable_random_scores(self, enabled: bool = True):
        """Enable or disable random score generation"""
        self.use_random_scores = enabled
        print(f"Random scores {'enabled' if enabled else 'disabled'}")
    
    def set_random_range(self, category: str, min_score: int, max_score: int):
        """Set custom random range for a category"""
        if category in self.random_ranges:
            self.random_ranges[category] = (min_score, max_score)
            print(f"Updated {category} range to {min_score}-{max_score}%")
    
    def normalize_skill(self, skill: str) -> str:
        """Normalize skill name by handling synonyms and variations"""
        skill_lower = skill.lower().strip()
        
        # Check for direct synonyms
        for main_skill, synonyms in self.skill_synonyms.items():
            if skill_lower == main_skill or skill_lower in synonyms:
                return main_skill
        
        return skill_lower
    
    def get_skill_category(self, skill: str) -> str:
        """Get the category of a skill"""
        normalized_skill = self.normalize_skill(skill)
        
        for category, skills in self.skill_categories.items():
            if normalized_skill in skills:
                return category
        
        return 'other'
    
    def advanced_skill_matching(self, resume_data: Dict, jd_data: Dict) -> Tuple[float, Dict]:
        """Advanced skill matching with categorization and weighting"""
        # Extract and normalize skills
        resume_skills = [self.normalize_skill(skill) for skill in resume_data.get('skills', [])]
        must_have_skills = [self.normalize_skill(skill) for skill in jd_data.get('must_have_skills', [])]
        good_to_have_skills = [self.normalize_skill(skill) for skill in jd_data.get('good_to_have_skills', [])]
        
        # Categorize skills
        resume_skill_categories = defaultdict(list)
        for skill in resume_skills:
            category = self.get_skill_category(skill)
            resume_skill_categories[category].append(skill)
        
        # Match must-have skills with advanced scoring
        matched_skills = []
        missing_skills = []
        skill_match_scores = {}
        
        for jd_skill in must_have_skills:
            best_match_score = 0
            best_match = None
            
            for resume_skill in resume_skills:
                # Exact match
                if jd_skill == resume_skill:
                    match_score = 1.0
                # Fuzzy match
                elif self.advanced_fuzzy_match(jd_skill, resume_skill):
                    match_score = 0.8
                # Category match (related skills)
                elif self.get_skill_category(jd_skill) == self.get_skill_category(resume_skill):
                    match_score = 0.6
                else:
                    match_score = 0
                
                if match_score > best_match_score:
                    best_match_score = match_score
                    best_match = resume_skill
            
            if best_match_score > 0.5:  # Threshold for considering a match
                matched_skills.append(jd_skill)
                skill_match_scores[jd_skill] = best_match_score
            else:
                missing_skills.append(jd_skill)
        
        # Calculate base skills score
        if must_have_skills:
            base_score = sum(skill_match_scores.values()) / len(must_have_skills)
        else:
            base_score = 0.5
        
        # Bonus calculations
        bonuses = self.calculate_skill_bonuses(resume_skills, must_have_skills, good_to_have_skills)
        
        # Apply bonuses
        final_score = min(base_score + bonuses['total_bonus'], 1.0)
        
        details = {
            'base_score': base_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'skill_match_scores': skill_match_scores,
            'bonuses': bonuses,
            'skill_categories_coverage': self.calculate_category_coverage(resume_skills, must_have_skills),
            'total_skills_required': len(must_have_skills),
            'skills_matched': len(matched_skills)
        }
        
        return final_score, details
    
    def calculate_skill_bonuses(self, resume_skills: List[str], must_have: List[str], good_to_have: List[str]) -> Dict:
        """Calculate various skill-based bonuses"""
        bonuses = {
            'good_to_have_bonus': 0,
            'diversity_bonus': 0,
            'expertise_bonus': 0,
            'total_bonus': 0
        }
        
        # Good-to-have skills bonus
        good_to_have_matches = 0
        for skill in good_to_have:
            if any(self.advanced_fuzzy_match(skill, r_skill) for r_skill in resume_skills):
                good_to_have_matches += 1
        
        if good_to_have:
            bonuses['good_to_have_bonus'] = (good_to_have_matches / len(good_to_have)) * 0.2
        
        # Skill diversity bonus (having skills across multiple categories)
        categories_covered = set()
        for skill in resume_skills:
            categories_covered.add(self.get_skill_category(skill))
        
        if len(categories_covered) >= 3:
            bonuses['diversity_bonus'] = self.scoring_params['skill_diversity_bonus']
        
        # Domain expertise bonus (having many skills in the same domain)
        category_counts = defaultdict(int)
        for skill in resume_skills:
            category_counts[self.get_skill_category(skill)] += 1
        
        max_category_count = max(category_counts.values()) if category_counts else 0
        if max_category_count >= 5:
            bonuses['expertise_bonus'] = self.scoring_params['domain_expertise_bonus']
        
        bonuses['total_bonus'] = sum([bonuses['good_to_have_bonus'], bonuses['diversity_bonus'], bonuses['expertise_bonus']])
        
        return bonuses
    
    def calculate_category_coverage(self, resume_skills: List[str], required_skills: List[str]) -> Dict:
        """Calculate how well resume covers different skill categories"""
        required_categories = set()
        covered_categories = set()
        
        for skill in required_skills:
            required_categories.add(self.get_skill_category(skill))
        
        for skill in resume_skills:
            skill_category = self.get_skill_category(skill)
            if skill_category in required_categories:
                covered_categories.add(skill_category)
        
        coverage_ratio = len(covered_categories) / len(required_categories) if required_categories else 1.0
        
        return {
            'required_categories': list(required_categories),
            'covered_categories': list(covered_categories),
            'coverage_ratio': coverage_ratio
        }
    
    def advanced_fuzzy_match(self, skill1: str, skill2: str, threshold: float = 0.75) -> bool:
        """Advanced fuzzy matching with context awareness"""
        # Exact match
        if skill1 == skill2:
            return True
        
        # Check synonyms
        skill1_normalized = self.normalize_skill(skill1)
        skill2_normalized = self.normalize_skill(skill2)
        
        if skill1_normalized == skill2_normalized:
            return True
        
        # Substring match for compound skills
        if len(skill1) > 3 and len(skill2) > 3:
            if skill1 in skill2 or skill2 in skill1:
                return True
        
        # Fuzzy match using sequence matcher
        similarity = SequenceMatcher(None, skill1, skill2).ratio()
        return similarity >= threshold
    
    def fuzzy_match(self, str1: str, str2: str, threshold: float = 0.8) -> bool:
        """Check if two strings are similar using fuzzy matching"""
        # Exact match
        if str1 == str2:
            return True
        
        # Substring match
        if str1 in str2 or str2 in str1:
            return True
        
        # Fuzzy match using sequence matcher
        similarity = SequenceMatcher(None, str1, str2).ratio()
        return similarity >= threshold
    
    def advanced_experience_evaluation(self, resume_data: Dict, jd_data: Dict) -> Tuple[float, Dict]:
        """Advanced experience evaluation with contextual analysis"""
        resume_experience = resume_data.get('experience', [])
        jd_experience_req = jd_data.get('experience_required', '')
        
        # Calculate total years of experience
        total_years = self.calculate_total_experience_years(resume_experience)
        required_years = self.extract_years_from_text(jd_experience_req)
        
        # Analyze experience relevance
        relevance_score = self.calculate_experience_relevance(resume_experience, jd_data)
        
        # Analyze experience level
        experience_level = self.determine_experience_level(resume_experience, jd_data)
        
        # Calculate progression score
        progression_score = self.calculate_career_progression(resume_experience)
        
        # Calculate recency score
        recency_score = self.calculate_experience_recency(resume_experience)
        
        # Base experience score
        if required_years > 0:
            years_score = min(total_years / required_years, 1.2)  # Allow 20% bonus for exceeding requirements
        else:
            years_score = 0.7  # Default score when no specific requirement
        
        # Weighted final score
        final_score = (
            years_score * 0.4 +
            relevance_score * 0.3 +
            progression_score * 0.2 +
            recency_score * 0.1
        )
        
        # Apply experience level bonus
        level_bonus = experience_level.get('bonus', 0)
        final_score = min(final_score + level_bonus, 1.0)
        
        details = {
            'total_years': total_years,
            'required_years': required_years,
            'years_score': years_score,
            'relevance_score': relevance_score,
            'progression_score': progression_score,
            'recency_score': recency_score,
            'experience_level': experience_level,
            'final_score': final_score
        }
        
        return final_score, details
    
    def calculate_total_experience_years(self, experience_list: List[Dict]) -> float:
        """Calculate total years of experience with overlap handling"""
        if not experience_list:
            return 0
        
        # Simple calculation - count each job as contributing experience
        # In a more advanced version, we could parse dates and handle overlaps
        total_years = 0
        for exp in experience_list:
            if isinstance(exp, dict):
                # Try to extract duration from description or assume 1-2 years per role
                duration = self.extract_duration_from_experience(exp)
                total_years += duration
        
        return total_years
    
    def extract_duration_from_experience(self, experience: Dict) -> float:
        """Extract duration from a single experience entry"""
        # Look for duration indicators in the description
        description = experience.get('description', '').lower()
        title = experience.get('title', '').lower()
        
        # Look for explicit duration mentions
        duration_patterns = [
            r'(\d+\.?\d*)\s*years?',
            r'(\d+)\s*months?',
            r'(\d+)\s*yrs?'
        ]
        
        for pattern in duration_patterns:
            matches = re.findall(pattern, description + ' ' + title)
            if matches:
                duration = float(matches[0])
                if 'month' in pattern:
                    duration = duration / 12  # Convert months to years
                return duration
        
        # Default assumption: 1.5 years per role if no explicit duration found
        return 1.5
    
    def calculate_experience_relevance(self, resume_experience: List[Dict], jd_data: Dict) -> float:
        """Calculate how relevant the experience is to the job requirements"""
        if not resume_experience:
            return 0.0
        
        jd_skills = set(self.normalize_skill(skill) for skill in jd_data.get('must_have_skills', []))
        jd_title = jd_data.get('title', '').lower()
        
        relevance_scores = []
        
        for exp in resume_experience:
            if not isinstance(exp, dict):
                continue
            
            exp_score = 0
            exp_title = exp.get('title', '').lower()
            exp_description = exp.get('description', '').lower()
            exp_company = exp.get('company', '').lower()
            
            # Title relevance
            title_similarity = SequenceMatcher(None, exp_title, jd_title).ratio()
            exp_score += title_similarity * 0.4
            
            # Skills mentioned in experience
            skills_mentioned = 0
            for skill in jd_skills:
                if skill in exp_description or skill in exp_title:
                    skills_mentioned += 1
            
            if jd_skills:
                skills_relevance = skills_mentioned / len(jd_skills)
                exp_score += skills_relevance * 0.6
            
            relevance_scores.append(exp_score)
        
        return sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0
    
    def determine_experience_level(self, resume_experience: List[Dict], jd_data: Dict) -> Dict:
        """Determine the experience level and calculate appropriate bonus"""
        jd_title = jd_data.get('title', '').lower()
        jd_description = jd_data.get('raw_text', '').lower()
        
        # Determine required level from JD
        required_level = 'mid'  # default
        for level, indicators in self.experience_indicators.items():
            if any(indicator in jd_title or indicator in jd_description for indicator in indicators):
                required_level = level
                break
        
        # Determine candidate's level from resume
        candidate_level_scores = {'junior': 0, 'mid': 0, 'senior': 0}
        
        for exp in resume_experience:
            if not isinstance(exp, dict):
                continue
            
            exp_title = exp.get('title', '').lower()
            exp_description = exp.get('description', '').lower()
            
            for level, indicators in self.experience_indicators.items():
                for indicator in indicators:
                    if indicator in exp_title or indicator in exp_description:
                        candidate_level_scores[level] += 1
        
        # Determine candidate's primary level
        candidate_level = max(candidate_level_scores, key=candidate_level_scores.get)
        
        # Calculate bonus based on level match
        level_match_bonus = 0
        if candidate_level == required_level:
            level_match_bonus = self.scoring_params['experience_level_bonus']
        elif (candidate_level == 'senior' and required_level == 'mid') or \
             (candidate_level == 'mid' and required_level == 'junior'):
            level_match_bonus = self.scoring_params['experience_level_bonus'] * 0.5
        
        return {
            'required_level': required_level,
            'candidate_level': candidate_level,
            'level_scores': candidate_level_scores,
            'bonus': level_match_bonus
        }
    
    def calculate_career_progression(self, resume_experience: List[Dict]) -> float:
        """Calculate career progression score"""
        if len(resume_experience) < 2:
            return 0.5  # Neutral score for single job
        
        # Look for progression indicators
        progression_indicators = ['promoted', 'advanced', 'lead', 'senior', 'manager', 'director']
        progression_score = 0
        
        for exp in resume_experience:
            if not isinstance(exp, dict):
                continue
            
            exp_text = (exp.get('title', '') + ' ' + exp.get('description', '')).lower()
            
            for indicator in progression_indicators:
                if indicator in exp_text:
                    progression_score += 0.2
        
        return min(progression_score, 1.0)
    
    def calculate_experience_recency(self, resume_experience: List[Dict]) -> float:
        """Calculate how recent and current the experience is"""
        # This is a simplified version - in practice, you'd parse actual dates
        # For now, assume the first experience in the list is the most recent
        
        if not resume_experience:
            return 0.0
        
        # Look for current job indicators
        recent_exp = resume_experience[0] if resume_experience else {}
        if isinstance(recent_exp, dict):
            description = recent_exp.get('description', '').lower()
            if 'current' in description or 'present' in description:
                return 1.0
        
        return 0.7  # Default score for recent experience
    
    def semantic_match_score(self, resume_data: Dict, jd_data: Dict) -> Tuple[float, Dict]:
        """Calculate semantic similarity using OpenAI embeddings or simple text matching"""
        if self.openai_client:
            return self.openai_semantic_match(resume_data, jd_data)
        else:
            return self.simple_semantic_match(resume_data, jd_data)
    
    def openai_semantic_match(self, resume_data: Dict, jd_data: Dict) -> Tuple[float, Dict]:
        """Calculate semantic similarity using OpenAI embeddings"""
        try:
            # Prepare texts
            resume_text = self.prepare_text_for_embedding(resume_data)
            jd_text = self.prepare_text_for_embedding(jd_data)
            
            # Get embeddings from OpenAI
            resume_embedding = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=resume_text
            ).data[0].embedding
            
            jd_embedding = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=jd_text
            ).data[0].embedding
            
            # Calculate cosine similarity
            similarity = self.cosine_similarity(resume_embedding, jd_embedding)
            
            return similarity, {'similarity': similarity, 'method': 'openai_embeddings'}
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to simple matching
            return self.simple_semantic_match(resume_data, jd_data)
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def simple_semantic_match(self, resume_data: Dict, jd_data: Dict) -> Tuple[float, Dict]:
        """Simple semantic matching using word overlap"""
        # Prepare texts
        resume_text = self.prepare_text_for_embedding(resume_data)
        jd_text = self.prepare_text_for_embedding(jd_data)
        
        # Tokenize and clean texts
        resume_words = self.tokenize_text(resume_text)
        jd_words = self.tokenize_text(jd_text)
        
        # Calculate Jaccard similarity
        resume_set = set(resume_words)
        jd_set = set(jd_words)
        
        intersection = len(resume_set.intersection(jd_set))
        union = len(resume_set.union(jd_set))
        
        if union == 0:
            similarity = 0.0
        else:
            similarity = intersection / union
        
        return similarity, {'similarity': similarity, 'method': 'simple_word_overlap'}
    
    def tokenize_text(self, text: str) -> List[str]:
        """Simple tokenization"""
        # Convert to lowercase and split by whitespace
        words = text.lower().split()
        # Remove stop words and short words
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        return words
    
    def prepare_text_for_embedding(self, data: Dict) -> str:
        """Prepare text for embedding by combining relevant fields"""
        text_parts = []
        
        # Add skills
        if 'skills' in data:
            text_parts.extend(data['skills'])
        
        # Add experience
        if 'experience' in data:
            for exp in data['experience']:
                if isinstance(exp, dict):
                    text_parts.append(exp.get('title', ''))
                    text_parts.append(exp.get('company', ''))
                    text_parts.append(exp.get('description', ''))
        
        # Add projects
        if 'projects' in data:
            for proj in data['projects']:
                if isinstance(proj, dict):
                    text_parts.append(proj.get('title', ''))
                    text_parts.append(proj.get('description', ''))
        
        # Add education
        if 'education' in data:
            for edu in data['education']:
                if isinstance(edu, dict):
                    text_parts.append(edu.get('degree', ''))
                    text_parts.append(edu.get('institution', ''))
        
        # Add summary
        if 'summary' in data and data['summary']:
            text_parts.append(data['summary'])
        
        # Add raw text
        if 'raw_text' in data:
            text_parts.append(data['raw_text'])
        
        return ' '.join(text_parts)
    
    def experience_match_score(self, resume_data: Dict, jd_data: Dict) -> Tuple[float, Dict]:
        """Calculate experience match score using advanced evaluation"""
        return self.advanced_experience_evaluation(resume_data, jd_data)
    
    def extract_years_from_text(self, text: str) -> int:
        """Extract number of years from text"""
        if not text:
            return 0
        
        # Look for patterns like "3+ years", "2-5 years", etc.
        patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\s*-\s*(\d+)\s*years?',
            r'minimum\s*(\d+)\s*years?',
            r'at\s*least\s*(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    return int(matches[0][0])  # Take minimum from range
                else:
                    return int(matches[0])
        
        return 0
    
    def education_match_score(self, resume_data: Dict, jd_data: Dict) -> Tuple[float, Dict]:
        """Calculate education match score"""
        resume_education = resume_data.get('education', [])
        jd_qualifications = jd_data.get('qualifications', [])
        
        if not jd_qualifications:
            return 0.5, {'resume_education': resume_education, 'required_qualifications': 'Not specified'}
        
        # Check if resume has any of the required qualifications
        resume_degrees = []
        for edu in resume_education:
            if isinstance(edu, dict):
                degree = edu.get('degree', '').lower()
                resume_degrees.append(degree)
        
        matches = 0
        for jd_qual in jd_qualifications:
            jd_qual_lower = jd_qual.lower()
            for resume_degree in resume_degrees:
                if jd_qual_lower in resume_degree or resume_degree in jd_qual_lower:
                    matches += 1
                    break
        
        score = matches / len(jd_qualifications) if jd_qualifications else 0.5
        
        return score, {'resume_education': resume_education, 'required_qualifications': jd_qualifications}
    
    def generate_advanced_suggestions(self, resume_data: Dict, jd_data: Dict, evaluation_details: Dict) -> List[str]:
        """Generate advanced personalized suggestions for improvement"""
        suggestions = []
        
        # Skills-based suggestions
        skills_details = evaluation_details.get('skills_match', {})
        missing_skills = skills_details.get('missing_skills', [])
        skill_categories = skills_details.get('skill_categories_coverage', {})
        
        if missing_skills:
            # Prioritize critical skills
            critical_skills = missing_skills[:3]
            suggestions.append(f"🎯 Priority Skills: Focus on learning {', '.join(critical_skills)} as they are critical for this role")
            
            # Category-based suggestions
            missing_categories = set(skill_categories.get('required_categories', [])) - set(skill_categories.get('covered_categories', []))
            if missing_categories:
                suggestions.append(f"📚 Skill Areas: Develop expertise in {', '.join(list(missing_categories)[:2])} domain(s)")
        
        # Experience-based suggestions
        exp_details = evaluation_details.get('experience_match', {})
        exp_level = exp_details.get('experience_level', {})
        
        if exp_level.get('candidate_level') != exp_level.get('required_level'):
            required_level = exp_level.get('required_level', 'mid')
            if required_level == 'senior':
                suggestions.append("🚀 Leadership: Highlight leadership, mentoring, or architectural decision-making experience")
            elif required_level == 'mid':
                suggestions.append("💼 Experience: Emphasize project ownership and technical problem-solving achievements")
        
        # Progression suggestions
        if exp_details.get('progression_score', 0) < 0.5:
            suggestions.append("📈 Career Growth: Highlight promotions, increased responsibilities, or skill advancement")
        
        # Domain expertise suggestions
        bonuses = skills_details.get('bonuses', {})
        if bonuses.get('expertise_bonus', 0) == 0:
            suggestions.append("🔧 Specialization: Develop deeper expertise in your strongest skill area")
        
        if bonuses.get('diversity_bonus', 0) == 0:
            suggestions.append("🌐 Versatility: Expand your skill set across different technology domains")
        
        # Semantic alignment suggestions
        semantic_score = evaluation_details.get('semantic_match', {}).get('similarity', 0)
        if semantic_score < 0.4:
            suggestions.append("✍️ Resume Optimization: Use more job-relevant keywords and phrases in your experience descriptions")
        
        # Project suggestions
        if not resume_data.get('projects', []):
            jd_skills = jd_data.get('must_have_skills', [])[:2]
            if jd_skills:
                suggestions.append(f"🛠️ Portfolio: Create projects showcasing {' and '.join(jd_skills)} to demonstrate practical skills")
        
        # Education alignment
        edu_details = evaluation_details.get('education_match', {})
        if edu_details.get('final_score', 0.5) < 0.7:
            suggestions.append("🎓 Certifications: Consider relevant certifications or courses to strengthen your qualifications")
        
        return suggestions[:6]  # Limit to 6 most impactful suggestions
    
    def determine_advanced_verdict(self, relevance_score: float, skills_score: float, experience_score: float) -> str:
        """Determine verdict based on multiple factors with non-linear evaluation"""
        # Non-linear scoring with different thresholds
        if relevance_score >= 85:
            return "Excellent Match"
        elif relevance_score >= 75:
            # Check if candidate excels in critical areas
            if skills_score >= 80 or experience_score >= 80:
                return "Strong Match"
            else:
                return "Good Match"
        elif relevance_score >= 60:
            # Check for potential with strong skills
            if skills_score >= 70:
                return "Potential Match"
            else:
                return "Moderate Match"
        elif relevance_score >= 40:
            return "Weak Match"
        else:
            return "Poor Match"
    
    def evaluate(self, resume_data: Dict, jd_data: Dict) -> Dict[str, Any]:
        """Advanced evaluation function with dynamic scoring"""
        try:
            # Check if random scores are enabled
            if self.use_random_scores:
                return self.generate_random_evaluation(resume_data, jd_data)
            
            # Use advanced skill matching
            skills_score, skills_details = self.advanced_skill_matching(resume_data, jd_data)
            
            # Use advanced experience evaluation
            experience_score, experience_details = self.advanced_experience_evaluation(resume_data, jd_data)
            
            # Use existing semantic and education matching
            semantic_score, semantic_details = self.semantic_match_score(resume_data, jd_data)
            education_score, education_details = self.education_match_score(resume_data, jd_data)
            
            # Dynamic weight adjustment based on job requirements
            adjusted_weights = self.calculate_dynamic_weights(jd_data)
            
            # Calculate weighted final score with non-linear adjustments
            base_score = (
                skills_score * adjusted_weights['skills_match'] +
                experience_score * adjusted_weights['experience_relevance'] +
                semantic_score * adjusted_weights['semantic_similarity'] +
                education_score * adjusted_weights['education_match']
            )
            
            # Apply non-linear transformations for better differentiation
            final_score = self.apply_scoring_curve(base_score, skills_score, experience_score)
            
            # Convert to percentage and round
            final_score_pct = round(final_score * 100, 2)
            skills_score_pct = round(skills_score * 100, 2)
            experience_score_pct = round(experience_score * 100, 2)
            
            # Determine advanced verdict
            verdict = self.determine_advanced_verdict(final_score_pct, skills_score_pct, experience_score_pct)
            
            # Compile detailed evaluation data
            evaluation_details = {
                'skills_match': skills_details,
                'experience_match': experience_details,
                'semantic_match': semantic_details,
                'education_match': education_details,
                'dynamic_weights': adjusted_weights,
                'scoring_breakdown': {
                    'base_score': base_score,
                    'final_score': final_score,
                    'score_adjustments': self.get_score_adjustments(skills_score, experience_score)
                }
            }
            
            # Generate advanced suggestions
            suggestions = self.generate_advanced_suggestions(resume_data, jd_data, evaluation_details)
            
            # Extract missing skills with priority
            missing_skills = skills_details.get('missing_skills', [])
            
            # Calculate match confidence
            match_confidence = self.calculate_match_confidence(skills_details, experience_details)
            
            return {
                'relevance_score': final_score_pct,
                'verdict': verdict,
                'match_confidence': match_confidence,
                'missing_skills': missing_skills,
                'suggestions': suggestions,
                'skills_match_score': skills_score_pct,
                'experience_match_score': experience_score_pct,
                'semantic_match_score': round(semantic_score * 100, 2),
                'education_match_score': round(education_score * 100, 2),
                'detailed_analysis': evaluation_details,
                'evaluation_summary': self.generate_evaluation_summary(
                    final_score_pct, skills_details, experience_details, verdict
                )
            }
        
        except Exception as e:
            print(f"Error in evaluation: {e}")
            import traceback
            traceback.print_exc()
            return {
                'relevance_score': 0.0,
                'verdict': 'Error',
                'match_confidence': 'Low',
                'missing_skills': [],
                'suggestions': ['Error occurred during evaluation. Please check the input data.'],
                'skills_match_score': 0.0,
                'experience_match_score': 0.0,
                'semantic_match_score': 0.0,
                'education_match_score': 0.0,
                'detailed_analysis': {},
                'evaluation_summary': 'Evaluation failed due to an error.'
            }
    
    def calculate_dynamic_weights(self, jd_data: Dict) -> Dict[str, float]:
        """Calculate dynamic weights based on job requirements"""
        weights = self.base_weights.copy()
        
        # Adjust weights based on job characteristics
        must_have_skills = jd_data.get('must_have_skills', [])
        experience_required = jd_data.get('experience_required', '')
        
        # If many skills are required, increase skills weight
        if len(must_have_skills) > 5:
            weights['skills_match'] += 0.1
            weights['semantic_similarity'] -= 0.05
            weights['education_match'] -= 0.05
        
        # If specific experience is heavily emphasized, increase experience weight
        if any(keyword in experience_required.lower() for keyword in ['senior', 'lead', 'architect', 'manager']):
            weights['experience_relevance'] += 0.1
            weights['skills_match'] -= 0.05
            weights['semantic_similarity'] -= 0.05
        
        # Normalize weights to sum to 1.0
        total_weight = sum(weights.values())
        for key in weights:
            weights[key] = weights[key] / total_weight
        
        return weights
    
    def apply_scoring_curve(self, base_score: float, skills_score: float, experience_score: float) -> float:
        """Apply non-linear scoring curve for better differentiation"""
        # Apply sigmoid-like curve to spread out scores
        adjusted_score = base_score
        
        # Bonus for high performers
        if base_score > 0.8:
            adjusted_score = base_score + (1 - base_score) * 0.3
        
        # Penalty for very low scores to create more separation
        elif base_score < 0.3:
            adjusted_score = base_score * 0.8
        
        # Boost candidates with exceptional skills even if other areas are weak
        if skills_score > 0.9:
            adjusted_score = min(adjusted_score + 0.1, 1.0)
        
        # Boost candidates with exceptional experience
        if experience_score > 0.9:
            adjusted_score = min(adjusted_score + 0.05, 1.0)
        
        return min(max(adjusted_score, 0.0), 1.0)
    
    def generate_random_evaluation(self, resume_data: Dict, jd_data: Dict) -> Dict[str, Any]:
        """Generate random evaluation results for demonstration purposes"""
        # Randomly select a performance category
        categories = list(self.random_ranges.keys())
        category = random.choice(categories)
        
        # Generate random scores within realistic ranges
        final_score = round(random.uniform(*self.random_ranges[category]), 2)
        skills_score = round(random.uniform(max(20, final_score - 15), min(100, final_score + 10)), 2)
        experience_score = round(random.uniform(max(15, final_score - 20), min(100, final_score + 15)), 2)
        semantic_score = round(random.uniform(max(10, final_score - 25), min(100, final_score + 5)), 2)
        education_score = round(random.uniform(max(30, final_score - 10), min(100, final_score + 20)), 2)
        
        # Generate random verdict based on score
        if final_score >= 85:
            verdicts = ["Excellent Match", "Strong Match"]
        elif final_score >= 75:
            verdicts = ["Strong Match", "Good Match"]
        elif final_score >= 65:
            verdicts = ["Good Match", "Potential Match"]
        elif final_score >= 55:
            verdicts = ["Potential Match", "Moderate Match"]
        elif final_score >= 45:
            verdicts = ["Moderate Match", "Weak Match"]
        else:
            verdicts = ["Weak Match", "Poor Match"]
        
        verdict = random.choice(verdicts)
        
        # Generate random confidence
        if final_score >= 80:
            confidence_options = ["Very High", "High"]
        elif final_score >= 60:
            confidence_options = ["High", "Medium"]
        elif final_score >= 40:
            confidence_options = ["Medium", "Low"]
        else:
            confidence_options = ["Low"]
        
        confidence = random.choice(confidence_options)
        
        # Generate random missing skills
        all_possible_skills = ['Python', 'Java', 'JavaScript', 'React', 'Angular', 'Node.js', 'Django', 'Flask', 
                              'PostgreSQL', 'MySQL', 'MongoDB', 'AWS', 'Docker', 'Kubernetes', 'Git', 'Linux']
        
        num_missing = random.randint(0, min(5, len(all_possible_skills)))
        missing_skills = random.sample(all_possible_skills, num_missing) if num_missing > 0 else []
        
        # Generate random suggestions
        suggestion_templates = [
            "🎯 Priority Skills: Focus on learning {skills} as they are critical for this role",
            "📚 Skill Areas: Develop expertise in {domain} domain",
            "🚀 Leadership: Highlight leadership, mentoring, or architectural decision-making experience",
            "💼 Experience: Emphasize project ownership and technical problem-solving achievements",
            "📈 Career Growth: Highlight promotions, increased responsibilities, or skill advancement",
            "🔧 Specialization: Develop deeper expertise in your strongest skill area",
            "🌐 Versatility: Expand your skill set across different technology domains",
            "✍️ Resume Optimization: Use more job-relevant keywords and phrases in your experience descriptions",
            "🛠️ Portfolio: Create projects showcasing {skills} to demonstrate practical skills",
            "🎓 Certifications: Consider relevant certifications or courses to strengthen your qualifications"
        ]
        
        num_suggestions = random.randint(3, 6)
        suggestions = []
        for _ in range(num_suggestions):
            template = random.choice(suggestion_templates)
            if '{skills}' in template:
                skills_sample = random.sample(['Python', 'React', 'AWS', 'Docker'], random.randint(1, 2))
                suggestion = template.format(skills=' and '.join(skills_sample))
            elif '{domain}' in template:
                domains = ['web development', 'cloud computing', 'data science', 'mobile development']
                suggestion = template.format(domain=random.choice(domains))
            else:
                suggestion = template
            suggestions.append(suggestion)
        
        # Generate evaluation summary
        summary_parts = [
            f"Overall Assessment: {verdict} ({final_score}%)",
            f"Skills Match: {random.randint(2, 8)}/{random.randint(5, 10)} required skills ({skills_score:.0f}%)"
        ]
        
        if missing_skills:
            summary_parts.append(f"Missing {len(missing_skills)} critical skill{'s' if len(missing_skills) > 1 else ''}")
        
        summary_parts.append(f"Experience Level: {random.choice(['Junior', 'Mid-level', 'Senior'])} candidate")
        
        evaluation_summary = " | ".join(summary_parts)
        
        return {
            'relevance_score': final_score,
            'verdict': verdict,
            'match_confidence': confidence,
            'missing_skills': missing_skills,
            'suggestions': suggestions,
            'skills_match_score': skills_score,
            'experience_match_score': experience_score,
            'semantic_match_score': semantic_score,
            'education_match_score': education_score,
            'evaluation_summary': evaluation_summary,
            'detailed_analysis': {
                'skills_match': {
                    'skills_matched': random.randint(2, 8),
                    'total_skills_required': random.randint(5, 10),
                    'bonuses': {
                        'good_to_have_bonus': random.uniform(0, 0.2),
                        'diversity_bonus': random.uniform(0, 0.1),
                        'expertise_bonus': random.uniform(0, 0.15),
                        'total_bonus': random.uniform(0, 0.3)
                    }
                },
                'experience_match': {
                    'total_years': random.randint(1, 8),
                    'required_years': random.randint(2, 5),
                    'experience_level': {
                        'candidate_level': random.choice(['junior', 'mid', 'senior']),
                        'required_level': random.choice(['junior', 'mid', 'senior'])
                    }
                }
            }
        }
    
    def hard_match_score(self, resume_data: Dict, jd_data: Dict) -> Tuple[float, Dict]:
        """Wrapper for backward compatibility - uses advanced skill matching"""
        return self.advanced_skill_matching(resume_data, jd_data)
    
    def get_score_adjustments(self, skills_score: float, experience_score: float) -> Dict:
        """Get details about score adjustments applied"""
        adjustments = {
            'high_performer_bonus': 0,
            'low_score_penalty': 0,
            'exceptional_skills_bonus': 0,
            'exceptional_experience_bonus': 0
        }
        
        if skills_score > 0.9:
            adjustments['exceptional_skills_bonus'] = 0.1
        
        if experience_score > 0.9:
            adjustments['exceptional_experience_bonus'] = 0.05
        
        return adjustments
    
    def calculate_match_confidence(self, skills_details: Dict, experience_details: Dict) -> str:
        """Calculate confidence level of the match"""
        skills_matched = skills_details.get('skills_matched', 0)
        total_skills = skills_details.get('total_skills_required', 1)
        experience_score = experience_details.get('final_score', 0)
        
        skill_coverage = skills_matched / total_skills if total_skills > 0 else 0
        
        if skill_coverage >= 0.8 and experience_score >= 0.8:
            return "Very High"
        elif skill_coverage >= 0.6 and experience_score >= 0.6:
            return "High"
        elif skill_coverage >= 0.4 or experience_score >= 0.6:
            return "Medium"
        else:
            return "Low"
    
    def generate_evaluation_summary(self, final_score: float, skills_details: Dict, 
                                  experience_details: Dict, verdict: str) -> str:
        """Generate a human-readable evaluation summary"""
        skills_matched = skills_details.get('skills_matched', 0)
        total_skills = skills_details.get('total_skills_required', 0)
        missing_skills = len(skills_details.get('missing_skills', []))
        
        summary_parts = []
        
        # Overall assessment
        summary_parts.append(f"Overall Assessment: {verdict} ({final_score}%)")
        
        # Skills summary
        if total_skills > 0:
            skill_percentage = (skills_matched / total_skills) * 100
            summary_parts.append(f"Skills Match: {skills_matched}/{total_skills} required skills ({skill_percentage:.0f}%)")
            
            if missing_skills > 0:
                summary_parts.append(f"Missing {missing_skills} critical skill{'s' if missing_skills > 1 else ''}")
        
        # Experience summary
        exp_level = experience_details.get('experience_level', {})
        candidate_level = exp_level.get('candidate_level', 'unknown')
        required_level = exp_level.get('required_level', 'unknown')
        
        if candidate_level != 'unknown' and required_level != 'unknown':
            if candidate_level == required_level:
                summary_parts.append(f"Experience Level: Perfect match ({candidate_level})")
            else:
                summary_parts.append(f"Experience Level: {candidate_level.title()} (requires {required_level})")
        
        return " | ".join(summary_parts)


# For backward compatibility
class RelevanceEngine(AdvancedRelevanceEngine):
    """Backward compatibility wrapper"""
    pass
