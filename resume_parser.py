import pdfplumber
from docx import Document
import re
import json
from typing import Dict, List, Any, Optional

class ResumeParser:
    def __init__(self):
        # Basic stop words list
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'i', 'me', 'my', 'myself', 'we', 'our',
            'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
            'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it',
            'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'will', 'shall'
        }
        
        # Common section headers
        self.section_headers = [
            'education', 'experience', 'work experience', 'employment',
            'skills', 'technical skills', 'core competencies',
            'projects', 'personal projects', 'academic projects',
            'certifications', 'certificates', 'awards', 'achievements',
            'summary', 'objective', 'profile', 'about', 'personal information'
        ]
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from file based on extension"""
        if file_path.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF or DOCX.")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)]', '', text)
        return text.strip()
    
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_pattern = r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        if phones:
            return ''.join(phones[0])
        return None
    
    def extract_name(self, text: str) -> str:
        """Extract name from resume (usually first line or after 'Name:')"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4:  # Name is usually short
                # Check if it looks like a name (contains letters, not just numbers/symbols)
                if re.search(r'[A-Za-z]', line) and not re.search(r'^\d+$', line):
                    return line
        return "Unknown"
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from resume"""
        sections = {}
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            is_header = False
            for header in self.section_headers:
                if header.lower() in line.lower():
                    # Save previous section
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = header.lower()
                    current_content = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def extract_skills(self, text: str, sections: Dict[str, str]) -> List[str]:
        """Extract skills from resume"""
        skills = []
        
        # Common technical skills
        technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'r',
            'html', 'css', 'bootstrap', 'sass', 'less', 'webpack', 'babel',
            'spring', 'django', 'flask', 'fastapi', 'express', 'laravel',
            'linux', 'ubuntu', 'centos', 'windows', 'macos'
        ]
        
        # Check skills section first
        if 'skills' in sections:
            skills_text = sections['skills'].lower()
            for skill in technical_skills:
                if skill in skills_text:
                    skills.append(skill.title())
        
        # Also check entire resume for skills
        text_lower = text.lower()
        for skill in technical_skills:
            if skill in text_lower and skill.title() not in skills:
                skills.append(skill.title())
        
        return skills
    
    def extract_education(self, sections: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract education information"""
        education = []
        
        if 'education' in sections:
            edu_text = sections['education']
            lines = edu_text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for degree patterns
                degree_patterns = [
                    r'(bachelor|b\.?s\.?|b\.?e\.?|b\.?tech)',
                    r'(master|m\.?s\.?|m\.?e\.?|m\.?tech)',
                    r'(phd|ph\.?d\.?|doctorate)',
                    r'(diploma|certificate)'
                ]
                
                for pattern in degree_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        education.append({
                            'degree': line,
                            'institution': '',
                            'year': ''
                        })
                        break
        
        return education
    
    def extract_experience(self, sections: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract work experience"""
        experience = []
        
        exp_sections = ['experience', 'work experience', 'employment']
        for section in exp_sections:
            if section in sections:
                exp_text = sections[section]
                lines = exp_text.split('\n')
                
                current_exp = {}
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Look for company names (usually in caps or title case)
                    if re.search(r'[A-Z][a-z]+', line) and len(line.split()) <= 5:
                        if 'company' not in current_exp:
                            current_exp['company'] = line
                        elif 'title' not in current_exp:
                            current_exp['title'] = line
                    
                    # Look for dates
                    date_pattern = r'\b(19|20)\d{2}\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b'
                    if re.search(date_pattern, line, re.IGNORECASE):
                        current_exp['duration'] = line
                
                if current_exp:
                    experience.append(current_exp)
        
        return experience
    
    def extract_projects(self, sections: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract project information"""
        projects = []
        
        if 'projects' in sections:
            proj_text = sections['projects']
            lines = proj_text.split('\n')
            
            current_proj = {}
            for line in lines:
                line = line.strip()
                if not line:
                    if current_proj:
                        projects.append(current_proj)
                        current_proj = {}
                    continue
                
                # Look for project titles (usually start with capital letter)
                if re.match(r'^[A-Z]', line) and len(line.split()) <= 8:
                    if current_proj:
                        projects.append(current_proj)
                    current_proj = {'title': line, 'description': ''}
                elif current_proj:
                    current_proj['description'] += line + ' '
            
            if current_proj:
                projects.append(current_proj)
        
        return projects
    
    def extract_certifications(self, sections: Dict[str, str]) -> List[str]:
        """Extract certifications"""
        certifications = []
        
        cert_sections = ['certifications', 'certificates', 'awards', 'achievements']
        for section in cert_sections:
            if section in sections:
                cert_text = sections[section]
                lines = cert_text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line and not line.lower().startswith(('certification', 'certificate', 'award')):
                        certifications.append(line)
        
        return certifications
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Main parsing function"""
        try:
            # Extract raw text
            raw_text = self.extract_text(file_path)
            if not raw_text:
                raise ValueError("Could not extract text from file")
            
            # Clean text
            cleaned_text = self.clean_text(raw_text)
            
            # Extract sections
            sections = self.extract_sections(cleaned_text)
            
            # Extract information
            name = self.extract_name(cleaned_text)
            email = self.extract_email(cleaned_text)
            phone = self.extract_phone(cleaned_text)
            skills = self.extract_skills(cleaned_text, sections)
            education = self.extract_education(sections)
            experience = self.extract_experience(sections)
            projects = self.extract_projects(sections)
            certifications = self.extract_certifications(sections)
            
            # Extract summary/objective
            summary = None
            for section in ['summary', 'objective', 'profile', 'about']:
                if section in sections:
                    summary = sections[section]
                    break
            
            return {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': skills,
                'education': education,
                'experience': experience,
                'projects': projects,
                'certifications': certifications,
                'summary': summary,
                'raw_text': cleaned_text
            }
        
        except Exception as e:
            print(f"Error parsing resume: {e}")
            return {
                'name': 'Unknown',
                'email': None,
                'phone': None,
                'skills': [],
                'education': [],
                'experience': [],
                'projects': [],
                'certifications': [],
                'summary': None,
                'raw_text': ''
            }
