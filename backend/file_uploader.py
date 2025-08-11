import os
import shutil
from typing import List
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

# Access variables from the .env file
# CANDIDATE_CV_FILE = os.getenv('CANDIDATE_CV_FILE_DIR')
# CANDIDATE_JD_FILE = os.getenv('CANDIDATE_JD_FILE_DIR')
# HR_CV_FILE = os.getenv('HR_CV_FILE_DIR')
# HR_JD_FILE = os.getenv('HR_JD_FILE_DIR')

CANDIDATE_CV_FILE = "./uploads/candidate/cv/"
CANDIDATE_JD_FILE = "./uploads/candidate/jd/"
HR_CV_FILE = "./uploads/hr/cv/"
HR_JD_FILE = "./uploads/hr/jd/"



# Make sure folders exist
os.makedirs(CANDIDATE_CV_FILE, exist_ok=True)
os.makedirs(CANDIDATE_JD_FILE, exist_ok=True)
os.makedirs(HR_CV_FILE, exist_ok=True)
os.makedirs(HR_JD_FILE, exist_ok=True)

async def save_candidate_files(pdf_file: UploadFile, jd_text: str):
    # Save PDF
    pdf_path = os.path.join(CANDIDATE_CV_FILE, "resume.pdf")
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(pdf_file.file, buffer)

    # Save JD text
    jd_path = os.path.join(CANDIDATE_JD_FILE, "jd.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(jd_text)

    return {"message": "Files uploaded successfully"}

async def save_hr_files(pdf_files: List[UploadFile], jd_text: str):
    # Save multiple PDFs
    pdf_paths = []
    for pdf_file in pdf_files:
        pdf_filename = pdf_file.filename  # Create unique filename for each PDF
        pdf_path = os.path.join(HR_CV_FILE, pdf_filename)
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)
        pdf_paths.append(pdf_path)  # Store the path for reference or logging

    # Save JD text
    jd_path = os.path.join(HR_JD_FILE, "jd.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(jd_text)

    return {"message": "Files uploaded successfully", "pdf_files": pdf_paths}