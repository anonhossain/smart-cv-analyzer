import csv
from io import BytesIO
import os
import re
from dotenv import load_dotenv
from fastapi import UploadFile
from fastapi.responses import JSONResponse
import pdfplumber
import pandas as pd

# Load environment variables
load_dotenv()

#HR_CV_FILES = os.getenv('HR_CV_FILES')  # Directory where the PDFs are stored
#OUTPUT_DIRECTORY = os.getenv('OUTPUT_DIRECTORY')  # Directory where CSV will be saved

OUTPUT_DIRECTORY = "./output"  # Directory where CSV will be saved
HR_CV_FILES= "./uploads/hr/cv/"  # Directory where the PDFs are stored

os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)  # Ensure the output directory exists

class ResumeExtractor:

    @staticmethod
    def extract_emails(text):
        """Extract email addresses from text."""
        return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

    @staticmethod
    def extract_phone_numbers(text):
        """Extract phone numbers from text."""
        return re.findall(r'\+?880[-\s]?\d{4}[-\s]?\d{6}|\d{5}[-\s]?\d{6}', text)

    @staticmethod
    def extract_text_from_pdf(resume_file_path):
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
    def read_file_content(file_path):
        """Read content from a PDF file."""
        try:
            if file_path.lower().endswith('.pdf'):
                return ResumeExtractor.extract_text_from_pdf(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    @staticmethod
    def extract_resume_info():
        resumes = []

        for file_name in os.listdir(HR_CV_FILES):
            file_path = os.path.join(HR_CV_FILES, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith('.pdf'):
                content = ResumeExtractor.read_file_content(file_path)
                if content:
                    resumes.append((file_name, content))

        info = {}

        for name, text in resumes:
            emails = ResumeExtractor.extract_emails(text)
            phones = ResumeExtractor.extract_phone_numbers(text)

            clean_name = name[:-4] if name.lower().endswith(".pdf") else name  # Remove .pdf

            info[clean_name] = {
                "candidate_email": emails[0] if emails else "No email found",
                "candidate_phone": phones[0] if phones else "No phone number found",
                "candidate_Ref_emails": emails[1:] if len(emails) > 1 else [],
                "candidate_Ref_phones": phones[1:] if len(phones) > 1 else []
            }

        # Write all data to a single CSV
        csv_file_path = os.path.join(OUTPUT_DIRECTORY, "resume_info.csv")
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ["Name", "Email", "Phone", "Reference Emails", "Reference Phones"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for file_name, details in info.items():
                writer.writerow({
                    "Name": file_name,
                    "Email": details["candidate_email"],
                    "Phone": details["candidate_phone"],
                    "Reference Emails": ", ".join(details["candidate_Ref_emails"]),
                    "Reference Phones": ", ".join(details["candidate_Ref_phones"])
                })

        print(f"CSV saved to: {csv_file_path}")
        return info
    
    @staticmethod
    async def get_excel_columns(file: UploadFile):
        try:
            contents = await file.read()
            filename = file.filename.lower()
            if filename.endswith('.csv'):
                df = pd.read_csv(BytesIO(contents))
            elif filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(BytesIO(contents), engine='openpyxl')
            else:
                raise ValueError("Unsupported file type. Only Excel and CSV are supported.")
            
            columns = list(df.columns)
            return {"columns": columns}
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"An error occurred: {str(e)}"})