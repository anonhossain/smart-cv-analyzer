import os
from pyexpat import model
from typing import List
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse
from clear_files import clear_all_uploads
from file_uploader import save_candidate_files, save_hr_files

api = APIRouter(prefix="/api")

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
        return JSONResponse(content={"message": "HR files uploaded successfully", "pdf_files": response['pdf_files']}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error uploading HR files", "error": str(e)}, status_code=500)    

@api.post("/clear-uploads")
def clear_uploads():
    result = clear_all_uploads()
    return JSONResponse(content=result)
