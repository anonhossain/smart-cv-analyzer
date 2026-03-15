import os

class routes:
    CANDIDATE_CV_FILE = os.getenv('CANDIDATE_CV_FILE')  # Path to the candidate's resume PDF
    CANDIDATE_JD_FILE = os.getenv('CANDIDATE_JD_FILE')  # Path to the candidate's job description text file
    MODEL = os.getenv("MODEL")