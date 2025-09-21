"""
Configuration settings for the Resume Evaluation System
"""

# Evaluation Settings
USE_RANDOM_SCORES = True  # Set to False for actual evaluation based on resume content

# Random Score Ranges (min, max) for different performance categories
RANDOM_SCORE_RANGES = {
    'excellent': (85, 95),
    'strong': (75, 84), 
    'good': (65, 74),
    'potential': (55, 64),
    'moderate': (45, 54),
    'weak': (30, 44),
    'poor': (15, 29)
}

# API Settings
OPENAI_API_KEY = None  # Set your OpenAI API key here if you have one

# Database Settings
DATABASE_URL = "sqlite:///./resume_evaluation.db"

# File Upload Settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

print(f"[DICE] Random Evaluation: {'ENABLED' if USE_RANDOM_SCORES else 'DISABLED'}")
print(f"[CHART] Score Ranges: {len(RANDOM_SCORE_RANGES)} categories configured")
