#!/usr/bin/env python3
"""
Run script for the Automated Resume Relevance Check System
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        sys.exit(1)

def download_spacy_model():
    """Download required spaCy model"""
    print("Downloading spaCy model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading spaCy model: {e}")
        print("You can install it manually with: python -m spacy download en_core_web_sm")

def create_directories():
    """Create necessary directories"""
    directories = [
        "uploads",
        "uploads/resumes", 
        "uploads/jd",
        "static",
        "static/js",
        "templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_openai_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("   The system will work with reduced functionality (TF-IDF only)")
        print("   To enable full AI features, set your OpenAI API key:")
        print("   export OPENAI_API_KEY=your_api_key_here")
    else:
        print("✅ OpenAI API key found")

def run_application():
    """Run the FastAPI application"""
    print("\n🚀 Starting the Resume Relevance Check System...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        import uvicorn
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except ImportError:
        print("❌ Error: uvicorn not found. Please install requirements first.")
        sys.exit(1)

def main():
    """Main setup and run function"""
    print("🎯 Automated Resume Relevance Check System")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install requirements
    install_requirements()
    
    # Download spaCy model
    download_spacy_model()
    
    # Check OpenAI key
    check_openai_key()
    
    # Run application
    run_application()

if __name__ == "__main__":
    main()
