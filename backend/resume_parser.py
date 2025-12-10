import os
from PyPDF2 import PdfReader
import docx2txt


def extract_resume_text(file_path: str) -> str:
    """
    Extract plain text from a PDF or DOCX resume.
    Returns a cleaned string (or empty string if nothing could be extracted).
    """

    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    try:
        #PDF
        if ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

        #DOC / DOCX
        elif ext in [".doc", ".docx"]:
            # docx2txt handles both docx and (some) doc
            text = docx2txt.process(file_path) or ""

        #Unsupported format
        else:
            return ""

    except Exception as e:
        # For debugging in the terminal if something goes wrong
        print(f"[resume_parser] Error while extracting text: {e}")
        return ""

    text = " ".join(text.split())
    return text