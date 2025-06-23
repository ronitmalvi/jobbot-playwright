from PyPDF2 import PdfReader

def parse_resume(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)