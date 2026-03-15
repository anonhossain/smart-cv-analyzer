# app/src/backend/services/resume_extractor.py
import os
import re
import pdfplumber
import sys

_ROOT_SRC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT_SRC not in sys.path:
    sys.path.insert(0, _ROOT_SRC)

from backend.core.config import settings

class ResumeExtractor:
    @staticmethod
    def extract_text_from_pdf(resume_file_path: str) -> str:
        """Extract text from the uploaded PDF resume using pdfplumber."""
        text = ""
        try:
            with pdfplumber.open(resume_file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        except Exception as e:
            print(f"Error extracting text from PDF {resume_file_path}: {e}")
        return text

    @staticmethod
    def extract_emails(text: str) -> list:
        """Extract email addresses from text."""
        return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

    @staticmethod
    def extract_phone_numbers(text: str) -> list:
        """Extract phone numbers from text (supports Bangladesh formats)."""
        return re.findall(r'\+?880[-\s]?\d{4}[-\s]?\d{6}|\d{5}[-\s]?\d{6}', text)

    @staticmethod
    def read_file_content(file_path: str) -> str:
        """Read content based on file extension."""
        if file_path.lower().endswith('.pdf'):
            return ResumeExtractor.extract_text_from_pdf(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            return ""
    
    @staticmethod # Added decorator so it works as a static call
    def extract_resume_data(resume_file_path: str) -> dict:
        """Extract relevant data from the resume and split primary from references."""
        text = ResumeExtractor.read_file_content(resume_file_path)
        if not text:
            return {
                "text": "",
                "email": "N/A", 
                "reference_emails": [], 
                "phone": "N/A", 
                "reference_phones": []
            }

        all_emails = ResumeExtractor.extract_emails(text)
        all_phones = ResumeExtractor.extract_phone_numbers(text)

        return {
            "text": text,
            # First one is primary, the rest go to reference list
            "email": all_emails[0] if all_emails else "N/A",
            "reference_emails": all_emails[1:] if len(all_emails) > 1 else [],
            
            "phone": all_phones[0] if all_phones else "N/A",
            "reference_phones": all_phones[1:] if len(all_phones) > 1 else []
        }
    
if __name__ == "__main__":
    # Example usage
    # Note: Ensure CANDIDATE_CV_PATH is defined in your settings or use a direct path for testing
    resume_path = os.path.join(settings.CANDIDATE_CV_PATH, "resume.pdf") 
    
    if os.path.exists(resume_path):
        extracted_data = ResumeExtractor.extract_resume_data(resume_path)
        print("--- Extracted Text ---")
        print(extracted_data["text"][:200], "...") # Print first 200 chars
        print("\n--- Contact Info ---")
        print(f"Primary Email: {extracted_data['email']}")
        print(f"Reference Emails: {extracted_data['reference_emails']}")
        print(f"Primary Phone: {extracted_data['phone']}")
        print(f"Reference Phones: {extracted_data['reference_phones']}")
    else:
        print(f"Test file not found at {resume_path}")