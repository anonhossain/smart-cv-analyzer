import os
from pyexpat import model
from typing import List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from user_controller import UserController
from dbhelper import DBHelper
from model import LoginRequest, RegisterRequest, UserOut, UserUpdate
from gemini import Gemini, GeminiHR, HR_question_generator
from emailsender import EmailSender
from resume_extractor import ResumeExtractor
from clear_files import clear_all_uploads
from file_uploader import save_candidate_files, save_hr_files

api = APIRouter(prefix="/api")

db = DBHelper()

@api.get("/")
def read_root():
    return {"msg": "Hello, CORS is working!"}

@api.get("/hello")
def hello():
    return {"message": "Hello, Anon!"}

# Endpoint to upload files (PDF and JD text)
@api.post("/candidate-upload")
async def upload_files(pdf_file: UploadFile = File(...), jd_text: str = Form(...)):
    try:
        # Call the function to save the uploaded files
        response = await save_candidate_files(pdf_file, jd_text)
        return JSONResponse(content={"data": response}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error uploading files", "error": str(e)}, status_code=500)

# Endpoint to process a resume based on an action
@api.post("/hr-upload/")
async def hr_upload(pdf_files: List[UploadFile] = File(...), jd_text: str = Form(...)):
    try:
        # Call the save_hr_files function to save the uploaded files
        response = await save_hr_files(pdf_files, jd_text)
        return JSONResponse(content={"message": "HR CV and JD uploaded successfully", "pdf_files": response['pdf_files']}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error uploading HR files", "error": str(e)}, status_code=500)    

@api.post("/clear-uploads")
def clear_uploads():
    result = clear_all_uploads()
    return JSONResponse(content=result)

@api.post("/extract_resume_info/")
async def get_resume_info():
    result = ResumeExtractor.extract_resume_info()
    return result

@api.post("/get_excel_columns/")
async def get_excel_columns(file: UploadFile = File(...)):
    return await ResumeExtractor.get_excel_columns(file)

@api.post("/send_emails/")
async def send_emails(
    subject: str = Form(...),
    email_col: str = Form(...),
    email_message: str = Form(...),
    file: UploadFile = Form(...)
):
    try:
        sender = EmailSender(subject, email_col, email_message, file)
        await sender.send_bulk_emails()
        return {"message": "Emails sent successfully!"}
    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An error occurred: {str(e)}"})
    
@api.get("/candidate-resume-process")
def process_resume():
    """Process the candidate's resume and job description."""
    try:
        response = Gemini.process_resume()
        return {"status": "success", "data": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@api.post("/candidate-upload/")
async def upload_candidate_files(
    job_desc: str = Form(...),
    resume: UploadFile = File(...)
):
    try:
        # Save resume file
        resume_path = f"uploads/candidate/cv/{resume.filename}"
        with open(resume_path, "wb") as f:
            f.write(await resume.read())

        # Save job description
        jd_path = "uploads/candidate/jd/jd.txt"
        with open(jd_path, "w") as f:
            f.write(job_desc)

        return {"status": "success", "message": "Files uploaded successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@api.get("/hr-resumes-sort")
def process_hr_resumes():
    try:
        result = GeminiHR.process_resume()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@api.post("/generate-hr-questions")
def generate_hr_questions():
    try:
        HR_question_generator.process_resumes()
        return {"status": "success", "message": "Questions generated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@api.post("/register")
def register_user(user: RegisterRequest):
    return UserController.register_user(user)

@api.post("/login")
def login_user(request: LoginRequest):
    return UserController.login(request.username, request.password)

@api.get("/users") 
def get_users():
    return UserController.get_users()

@api.get("/delete-users/{user_id}")
def delete_user(user_id: int):
    return UserController.delete_user(user_id)

@api.get("/info")
def dashboardinfo():
    users = db.get_all_users()  # ✅ now exists
    roles = [user["role"].lower() for user in users]

    return {
        "candidate": roles.count("candidate"),
        "hr": roles.count("hr"),
        "admin": roles.count("admin"),
    }

@api.patch("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    if not db.get_user_by_id(user_id):
        raise HTTPException(status_code=404, detail="User not found")

    if not db.update_user(user_id, user.dict()):
        raise HTTPException(status_code=500, detail="Failed to update user")

    return UserOut(id=user_id, **user.dict())

from fastapi import FastAPI
from fastapi.responses import FileResponse
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "output", "selected_cvs")

@api.get("/api/download_cv/{cv_name}")
async def download_cv(cv_name: str):
    cv_path = os.path.join(UPLOAD_DIR, cv_name)
    if not os.path.exists(cv_path):
        return {"error": "File not found"}
    return FileResponse(cv_path, filename=cv_name)



