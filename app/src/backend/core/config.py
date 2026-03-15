import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Project Directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    # Candidate Paths
    CANDIDATE_CV_PATH: str = os.path.join(BASE_DIR, "uploads", "candidate", "cv")
    CANDIDATE_JD_PATH: str = os.path.join(BASE_DIR, "uploads", "candidate", "jd")
    
    # HR Paths
    HR_CV_DIR: str = "./uploads/hr/cv/"
    HR_JD_DIR: str = "./uploads/hr/jd/"
    OUTPUT_DIR: str = "./output"

    # Email Configurations
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_USER: str = os.getenv("SMTP_USERNAME", "your_email@gmail.com")
    SMTP_PASS: str = os.getenv("SMTP_PASSWORD") # From .env
    SMTP_PORT: int = 465

    # AI Model Configurations
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME: str = "gemini-1.5-flash"

    # Database Configurations
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "123"
    DB_NAME: str = "smart_resume_analyzer"

# Initialize the settings object
settings = Settings()