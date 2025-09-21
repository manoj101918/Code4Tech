# Automated Resume Relevance Check System

An AI-powered resume evaluation system that automatically matches resumes against job descriptions and provides relevance scores, missing skills analysis, and personalized improvement suggestions.

## Features

- **Resume Parsing**: Extract text from PDF and DOCX files
- **Job Description Analysis**: Parse and extract key requirements
- **Hybrid Scoring**: Combines hard keyword matching with semantic similarity
- **Relevance Scoring**: 0-100 score with High/Medium/Low verdict
- **Missing Skills Detection**: Identifies gaps in candidate profiles
- **Personalized Suggestions**: AI-generated improvement recommendations
- **Web Dashboard**: Modern, responsive interface for placement teams
- **Batch Processing**: Handle multiple resumes and job descriptions
- **Filtering & Search**: Advanced filtering by score, verdict, location
- **Export Functionality**: Download results as CSV

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight database
- **PyMuPDF**: PDF text extraction
- **python-docx**: DOCX text extraction
- **spaCy**: Natural language processing
- **scikit-learn**: Machine learning utilities
- **OpenAI**: LLM integration for semantic matching

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Bootstrap 5**: Responsive UI framework
- **JavaScript**: Interactive functionality
- **Font Awesome**: Icons

### AI/ML Components
- **TF-IDF**: Keyword-based matching
- **Cosine Similarity**: Semantic similarity
- **OpenAI Embeddings**: Advanced semantic understanding
- **Fuzzy Matching**: Flexible skill matching

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume-relevance-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the dashboard**
   Open your browser and go to: `http://localhost:8000`

## Usage

### 1. Upload Job Description
- Navigate to "Upload Job Description"
- Select a PDF, DOCX, or TXT file
- Enter job title and location
- Click "Upload Job Description"

### 2. Upload Resume
- Navigate to "Upload Resume"
- Select a PDF or DOCX file
- Enter student name and email
- Click "Upload Resume"

### 3. Evaluate Resume
- Navigate to "Evaluate"
- Select a resume and job description
- Click "Evaluate Resume"
- View detailed results with score breakdown

### 4. View Results
- Navigate to "Results"
- Filter by job description, score, or verdict
- View detailed evaluation reports
- Export results as CSV

## API Endpoints

### Resume Management
- `POST /upload/resume` - Upload and parse resume
- `GET /resumes` - Get all resumes

### Job Description Management
- `POST /upload/job-description` - Upload and parse job description
- `GET /job-descriptions` - Get all job descriptions

### Evaluation
- `POST /evaluate/{resume_id}/{jd_id}` - Evaluate resume against job description
- `GET /evaluations` - Get all evaluations with optional filters
- `GET /evaluation/{evaluation_id}` - Get detailed evaluation

## Scoring Algorithm

The system uses a hybrid approach combining multiple scoring methods:

### 1. Hard Match (40% weight)
- Exact keyword matching
- Fuzzy string matching for skills
- Required vs. good-to-have skills differentiation

### 2. Semantic Match (40% weight)
- OpenAI embeddings for contextual understanding
- TF-IDF fallback for semantic similarity
- Cosine similarity calculation

### 3. Experience Match (10% weight)
- Years of experience comparison
- Pattern recognition for experience requirements

### 4. Education Match (10% weight)
- Qualification requirements matching
- Degree level comparison

## File Structure

```
resume-relevance-system/
├── app.py                 # FastAPI application
├── database.py            # Database models and connection
├── models.py              # Pydantic models
├── resume_parser.py       # Resume text extraction and parsing
├── jd_parser.py          # Job description parsing
├── relevance_engine.py    # Scoring and evaluation logic
├── utils.py               # Utility functions
├── requirements.txt      # Python dependencies
├── templates/
│   └── dashboard.html     # Main dashboard template
├── static/
│   └── js/
│       └── dashboard.js   # Frontend JavaScript
└── uploads/               # File upload directory
    ├── resumes/          # Resume files
    └── jd/               # Job description files
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for semantic matching (optional)

### Scoring Weights
Modify weights in `relevance_engine.py`:
```python
self.weights = {
    'hard_match': 0.4,      # Keyword matching
    'semantic_match': 0.4,   # Semantic similarity
    'experience_match': 0.1, # Experience comparison
    'education_match': 0.1   # Education matching
}
```

## Troubleshooting

### Common Issues

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **OpenAI API errors**
   - Ensure API key is set correctly
   - Check API quota and billing
   - System will fallback to TF-IDF if OpenAI unavailable

3. **File upload issues**
   - Check file size (max 10MB)
   - Ensure file format is supported (PDF, DOCX, TXT)
   - Verify file is not corrupted

4. **Database errors**
   - Delete `resume_evaluation.db` to reset database
   - Ensure write permissions in project directory

### Performance Optimization

1. **Large file processing**
   - Consider file size limits
   - Implement async processing for large batches

2. **Database optimization**
   - Add indexes for frequently queried fields
   - Consider PostgreSQL for production

3. **Memory usage**
   - Process files in chunks
   - Clear temporary data after processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## Roadmap

### Phase 1 (Current)
- ✅ Basic resume parsing
- ✅ Job description analysis
- ✅ Hybrid scoring system
- ✅ Web dashboard

### Phase 2 (Future)
- 🔄 Batch processing
- 🔄 Advanced analytics
- 🔄 Integration with ATS systems
- 🔄 Machine learning model training

### Phase 3 (Future)
- 🔄 Real-time notifications
- 🔄 Advanced reporting
- 🔄 API rate limiting
- 🔄 Multi-tenant support
