from PyPDF2 import PdfReader

def parse_resume(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])