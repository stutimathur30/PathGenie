from PyPDF2 import PdfReader
from docx import Document

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'doc', 'txt'}

def extract_text_from_file(filepath):
    """Extract text from PDF, DOCX, or TXT files"""
    try:
        if filepath.endswith('.pdf'):
            with open(filepath, 'rb') as f:
                reader = PdfReader(f)
                text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif filepath.endswith(('.docx', '.doc')):
            doc = Document(filepath)
            text = " ".join([para.text for para in doc.paragraphs if para.text])
        else:  # Assume plain text
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from file: {str(e)}")