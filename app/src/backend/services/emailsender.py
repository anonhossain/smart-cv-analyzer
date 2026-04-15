# app/src/backend/services/email_sender.py
import smtplib
import os, sys
import pandas as pd
from io import BytesIO
from email.mime.text import MIMEText
from fastapi import UploadFile

_ROOT_SRC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT_SRC not in sys.path:
    sys.path.insert(0, _ROOT_SRC)
    
from backend.core.config import settings

class EmailSender:
    SMTP_SERVER = settings.SMTP_SERVER
    SMTP_USERNAME = settings.SMTP_USER
    SMTP_PASSWORD = settings.SMTP_PASS
    OUTPUT_DIR = settings.OUTPUT_DIR

    def __init__(self, subject: str, email_col: str, email_message: str, file: UploadFile):
        self.subject = subject
        self.email_col = email_col
        self.email_message = email_message
        self.file = file
        self.df = None

    async def load_data(self):
        """Reads file and initializes the dataframe with a status column."""
        contents = await self.file.read()
        filename = self.file.filename.lower()
        
        if filename.endswith('.csv'):
            self.df = pd.read_csv(BytesIO(contents))
        else:
            self.df = pd.read_excel(BytesIO(contents), engine='openpyxl')
        
        if self.email_col not in self.df.columns:
            raise ValueError(f"Column '{self.email_col}' missing.")
            
        # Initialize the status column
        self.df["Mail_status"] = "Pending"

    def get_customized_body(self, row: pd.Series) -> str:
        """Handles placeholder replacement."""
        message = self.email_message.replace("%7B", "{").replace("%7D", "}")
        for col in self.df.columns:
            if col != "Mail_status":
                message = message.replace(f"{{{col}}}", str(row[col]))
        return message

    def send_to_row(self, server: smtplib.SMTP_SSL, index: int):
        """Sends mail and updates the DataFrame status for a specific row."""
        row = self.df.loc[index]
        to_address = str(row[self.email_col]).strip()

        if not to_address or to_address.lower() == "nan":
            self.df.at[index, "Mail_status"] = "Failed: Invalid Email"
            return

        try:
            body = self.get_customized_body(row)
            msg = MIMEText(body)
            msg["Subject"] = self.subject
            msg["From"] = self.SMTP_USERNAME
            msg["To"] = to_address
            
            server.sendmail(self.SMTP_USERNAME, to_address, msg.as_string())
            self.df.at[index, "Mail_status"] = "Sent"
        except Exception as e:
            print(f"Error for {to_address}: {e}")
            self.df.at[index, "Mail_status"] = f"Failed: {str(e)}"

    def process_all_emails(self, server: smtplib.SMTP_SSL):
        """Iterates through indexes to allow direct DataFrame updates."""
        for index in self.df.index:
            self.send_to_row(server, index)

    def save_updated_report(self):
        """Saves the final result to a new CSV file."""
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        report_path = os.path.join(self.OUTPUT_DIR, "mail_delivery_report.csv")
        self.df.to_csv(report_path, index=False)
        print(f"Report saved to {report_path}")

    def execute_bulk_send(self):
        """Manages SMTP connection and triggers processing."""
        with smtplib.SMTP_SSL(self.SMTP_SERVER, 465) as server:
            server.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
            self.process_all_emails(server)

    async def run_orchestrator(self):
        """
        The Master Orchestrator.
        Strictly calling functions to manage the workflow.
        """
        await self.load_data()
        self.execute_bulk_send()
        self.save_updated_report()

if __name__ == "__main__":
    EmailSender().run_orchestrator()