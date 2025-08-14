import os
from pyexpat import model
from typing import List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from user_controller import UserController
from dbhelper import DBHelper
from model import RegisterRequest
from gemini import Gemini, GeminiHR, HR_question_generator
from emailsender import EmailSender
from resume_extractor import ResumeExtractor
from clear_files import clear_all_uploads
from file_uploader import save_candidate_files, save_hr_files

api = APIRouter(prefix="/api")

db = DBHelper()

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
    
@api.post("/hr-resumes-sort")
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

@api.get("/users") 
def get_users():
    return UserController.get_users()


@api.get("/delete-users/{user_id}")
def delete_user(user_id: int):
    return UserController.delete_user(user_id)

@api.get("/info")
def dashboardinfo():
    
    db.mycursor.execute("SELECT * FROM users")
    users = db.mycursor.fetchall()
    candidate = 0
    admin = 0
    hr = 0
    for user in users:
        if user[7] == 'Candidate':
            candidate += 1
        if user[7] == 'Admin':
            admin += 1
        if user[7] == 'HR':
            hr += 1
    
    return {"candidate": candidate, "admin": admin, "hr": hr}