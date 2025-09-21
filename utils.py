import os
from typing import Optional

def create_upload_dir():
    """Create upload directories if they don't exist"""
    directories = ['uploads', 'uploads/resumes', 'uploads/jd']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def allowed_file(filename: str, allowed_extensions: list) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def clean_filename(filename: str) -> str:
    """Clean filename for safe storage"""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    
    return filename

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    import re
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # Check if it has 10 digits (for Indian numbers)
    return len(digits) == 10

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_date(date_obj) -> str:
    """Format date object to string"""
    if date_obj is None:
        return "N/A"
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")

def get_score_color(score: float) -> str:
    """Get color class based on score"""
    if score >= 80:
        return "success"  # Green
    elif score >= 60:
        return "warning"  # Yellow
    else:
        return "danger"   # Red

def get_verdict_color(verdict: str) -> str:
    """Get color class based on verdict"""
    verdict_colors = {
        "High": "success",
        "Medium": "warning", 
        "Low": "danger"
    }
    return verdict_colors.get(verdict, "secondary")
