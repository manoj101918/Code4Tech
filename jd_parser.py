import re
import json
from typing import Dict, List, Any, Optional

class JobDescriptionParser:
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
        
        # Common job description sections
        self.section_headers = [
            'job title', 'position', 'role', 'title',
            'company', 'organization', 'employer',
            'location', 'work location', 'office location',
            'job type', 'employment type', 'work type',
            'experience', 'years of experience', 'experience required',
            'qualifications', 'requirements', 'must have', 'required',
            'skills', 'technical skills', 'core competencies',
            'responsibilities', 'duties', 'key responsibilities',
            'benefits', 'compensation', 'salary', 'package',
            'description', 'about the role', 'job description'
        ]
        
        # Common skill keywords
        self.technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'r',
            'html', 'css', 'bootstrap', 'sass', 'less', 'webpack', 'babel',
            'spring', 'django', 'flask', 'fastapi', 'express', 'laravel',
            'linux', 'ubuntu', 'centos', 'windows', 'macos', 'agile', 'scrum'
        ]
        
        # Qualification keywords
        self.qualification_keywords = [
            'bachelor', 'master', 'phd', 'degree', 'diploma', 'certification',
            'b.tech', 'b.e', 'm.tech', 'm.e', 'b.s', 'm.s', 'mba', 'bca', 'mca'
        ]
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from file (assuming it's already text or can be read directly)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                return ""
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)]', '', text)
        return text.strip()
    
    def extract_title(self, text: str) -> str:
        """Extract job title from text"""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line.split()) <= 8:  # Title is usually short
                # Look for common title patterns
                if any(word in line.lower() for word in ['engineer', 'developer', 'analyst', 'manager', 'specialist', 'consultant']):
                    return line
        return "Unknown Position"
    
    def extract_company(self, text: str) -> Optional[str]:
        """Extract company name from text"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 5:  # Company name is usually short
                # Look for company indicators
                if any(word in line.lower() for word in ['inc', 'ltd', 'corp', 'company', 'technologies', 'solutions']):
                    return line
        return None
    
    def extract_location(self, text: str) -> str:
        """Extract job location from text"""
        # Look for location patterns
        location_patterns = [
            r'(hyderabad|bangalore|pune|delhi|mumbai|chennai|kolkata|gurgaon|noida)',
            r'(remote|work from home|wfh)',
            r'(on-site|onsite|office)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].title()
        
        return "Not specified"
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from job description"""
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
    
    def extract_skills(self, text: str, sections: Dict[str, str]) -> Dict[str, List[str]]:
        """Extract skills from job description"""
        must_have_skills = []
        good_to_have_skills = []
        
        # Check skills sections
        skills_sections = ['skills', 'technical skills', 'core competencies', 'requirements']
        for section in skills_sections:
            if section in sections:
                skills_text = sections[section].lower()
                
                # Look for must-have indicators
                if any(word in skills_text for word in ['required', 'must have', 'essential', 'mandatory']):
                    for skill in self.technical_skills:
                        if skill in skills_text and skill not in must_have_skills:
                            must_have_skills.append(skill.title())
                else:
                    # Default to good-to-have if no specific indicators
                    for skill in self.technical_skills:
                        if skill in skills_text and skill not in good_to_have_skills:
                            good_to_have_skills.append(skill.title())
        
        # Also check entire text for skills
        text_lower = text.lower()
        for skill in self.technical_skills:
            if skill in text_lower:
                # Check if it's marked as required
                skill_context = self.get_skill_context(text, skill)
                if any(word in skill_context.lower() for word in ['required', 'must have', 'essential', 'mandatory']):
                    if skill.title() not in must_have_skills:
                        must_have_skills.append(skill.title())
                elif skill.title() not in good_to_have_skills and skill.title() not in must_have_skills:
                    good_to_have_skills.append(skill.title())
        
        return {
            'must_have': must_have_skills,
            'good_to_have': good_to_have_skills
        }
    
    def get_skill_context(self, text: str, skill: str) -> str:
        """Get context around a skill mention"""
        pattern = rf'.{{0,50}}{re.escape(skill)}.{{0,50}}'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return ' '.join(matches)
    
    def extract_qualifications(self, text: str, sections: Dict[str, str]) -> List[str]:
        """Extract educational qualifications"""
        qualifications = []
        
        # Check qualifications section
        if 'qualifications' in sections or 'requirements' in sections:
            qual_text = sections.get('qualifications', '') + ' ' + sections.get('requirements', '')
            for qual in self.qualification_keywords:
                if qual in qual_text.lower():
                    qualifications.append(qual.title())
        
        # Also check entire text
        text_lower = text.lower()
        for qual in self.qualification_keywords:
            if qual in text_lower and qual.title() not in qualifications:
                qualifications.append(qual.title())
        
        return qualifications
    
    def extract_experience_required(self, text: str) -> Optional[str]:
        """Extract experience requirements"""
        # Look for experience patterns
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\s*-\s*(\d+)\s*years?\s*(?:of\s*)?experience',
            r'minimum\s*(\d+)\s*years?\s*(?:of\s*)?experience',
            r'at\s*least\s*(\d+)\s*years?\s*(?:of\s*)?experience'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    return f"{matches[0][0]}-{matches[0][1]} years"
                else:
                    return f"{matches[0]}+ years"
        
        return None
    
    def extract_job_type(self, text: str) -> Optional[str]:
        """Extract job type (full-time, part-time, contract, etc.)"""
        job_types = ['full-time', 'part-time', 'contract', 'internship', 'remote', 'hybrid']
        text_lower = text.lower()
        
        for job_type in job_types:
            if job_type in text_lower:
                return job_type.title()
        
        return None
    
    def extract_description(self, text: str, sections: Dict[str, str]) -> str:
        """Extract job description"""
        # Look for description section
        desc_sections = ['description', 'about the role', 'job description']
        for section in desc_sections:
            if section in sections:
                return sections[section]
        
        # If no specific section, return first few paragraphs
        lines = text.split('\n')
        description_lines = []
        for line in lines[:20]:  # First 20 lines
            line = line.strip()
            if line and len(line) > 20:  # Skip short lines
                description_lines.append(line)
        
        return '\n'.join(description_lines[:5])  # First 5 substantial lines
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Main parsing function"""
        try:
            # Extract raw text
            raw_text = self.extract_text_from_file(file_path)
            if not raw_text:
                raise ValueError("Could not extract text from file")
            
            # Clean text
            cleaned_text = self.clean_text(raw_text)
            
            # Extract sections
            sections = self.extract_sections(cleaned_text)
            
            # Extract information
            title = self.extract_title(cleaned_text)
            company = self.extract_company(cleaned_text)
            location = self.extract_location(cleaned_text)
            skills = self.extract_skills(cleaned_text, sections)
            qualifications = self.extract_qualifications(cleaned_text, sections)
            experience_required = self.extract_experience_required(cleaned_text)
            job_type = self.extract_job_type(cleaned_text)
            description = self.extract_description(cleaned_text, sections)
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'must_have_skills': skills['must_have'],
                'good_to_have_skills': skills['good_to_have'],
                'qualifications': qualifications,
                'experience_required': experience_required,
                'job_type': job_type,
                'description': description,
                'raw_text': cleaned_text
            }
        
        except Exception as e:
            print(f"Error parsing job description: {e}")
            return {
                'title': 'Unknown Position',
                'company': None,
                'location': 'Not specified',
                'must_have_skills': [],
                'good_to_have_skills': [],
                'qualifications': [],
                'experience_required': None,
                'job_type': None,
                'description': '',
                'raw_text': ''
            }
