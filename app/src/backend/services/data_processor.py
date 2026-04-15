# app/src/backend/services/data_processor.py
import os
import sys
import pandas as pd

_ROOT_SRC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT_SRC not in sys.path:
    sys.path.insert(0, _ROOT_SRC)

from backend.core.config import settings
from backend.services.resume_extractor import ResumeExtractor

class DataProcessor:
    # Use settings for single source of truth
    OUTPUT_DIRECTORY = settings.OUTPUT_DIR
    HR_CV_FILES = settings.HR_CV_DIR
    CSV_PATH = os.path.join(settings.OUTPUT_DIR, "resume_info.csv")

    @classmethod
    def ensure_directions(cls):
        """Ensures the required input and output directories exist."""
        os.makedirs(cls.OUTPUT_DIRECTORY, exist_ok=True)
        os.makedirs(cls.HR_CV_FILES, exist_ok=True)
        print(f"Directories verified: {cls.OUTPUT_DIRECTORY}, {cls.HR_CV_FILES}")

    @classmethod
    def input_data(cls):
        """
        Scans the HR folder, uses ResumeExtractor to parse PDFs,
        and prepares a list of dictionaries for CSV conversion.
        """
        all_resumes_data = []

        # Check if the directory exists before listing
        if not os.path.exists(cls.HR_CV_FILES):
            print(f"Error: Directory not found: {cls.HR_CV_FILES}")
            return []

        # Iterate through files in the CV folder
        for file_name in os.listdir(cls.HR_CV_FILES):
            file_path = os.path.join(cls.HR_CV_FILES, file_name)
            
            # Only process PDF files
            if os.path.isfile(file_path) and file_name.lower().endswith('.pdf'):
                # Extract data using the updated static method
                data = ResumeExtractor.extract_resume_data(file_path)
                
                # Get the name of the PDF without extension
                clean_name = os.path.splitext(file_name)[0]

                # Map to the new keys returned by ResumeExtractor
                all_resumes_data.append({
                    "Name": clean_name,
                    "Email": data["email"],
                    "Phone": data["phone"],
                    "Reference Emails": ", ".join(data["reference_emails"]) if data["reference_emails"] else "None",
                    "Reference Phones": ", ".join(data["reference_phones"]) if data["reference_phones"] else "None"
                })
        
        return all_resumes_data

    @classmethod
    def create_csv_file(cls, resume_list: list):
        """
        Takes the extracted list and saves it to a CSV with specific headings.
        """
        if not resume_list:
            print("No data found to save. Please check if PDFs are in the folder.")
            return False

        # Define specific columns as requested
        columns = ["Name", "Email", "Phone", "Reference Emails", "Reference Phones"]
        
        # Create DataFrame and save
        df = pd.DataFrame(resume_list, columns=columns)
        df.to_csv(cls.CSV_PATH, index=False, encoding='utf-8')
        
        print(f"Success! {len(resume_list)} resumes processed.")
        print(f"CSV created at: {cls.CSV_PATH}")
        return True

    @classmethod
    def csv_generator_pipeline(cls):
        """Orchestrates the entire process."""
        cls.ensure_directions()
        extracted_list = cls.input_data()
        cls.create_csv_file(extracted_list)

if __name__ == "__main__":
    # Test the processor
    DataProcessor.csv_generator_pipeline()