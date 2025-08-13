import os
from pyexpat import model
from typing import List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
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
    # Check if the username or email already exists
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (user.username, user.email))
    existing_user = cursor.fetchone()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Register the new user
    user_id = db.register_user(
        user.first_name, 
        user.last_name, 
        user.username, 
        user.phone, 
        user.email, 
        user.password, 
        user.role
    )

    if user_id:
        return {"message": "User registered successfully!"}
    else:
        raise HTTPException(status_code=500, detail="User registration failed")

@api.get("/users")
def get_users():
    db = DBHelper()
    db.mycursor.execute("SELECT * FROM users")
    users = db.mycursor.fetchall()
    return users