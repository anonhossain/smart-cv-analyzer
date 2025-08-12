from email.mime.text import MIMEText
import os
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
import pandas as pd
import smtplib
import re
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    print(SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD)
 
    def __init__(self, subject: str, email_col: str, email_message: str, file: UploadFile):
        self.subject = subject
        self.email_col = email_col
        self.email_message = email_message
        self.file = file
        self.df = None
        
    async def read_file(self):
        contents = await self.file.read()
        filename = self.file.filename.lower()
        if filename.endswith('.csv'):
            self.df = pd.read_csv(BytesIO(contents))
        elif filename.endswith(('.xls', '.xlsx')):
            self.df = pd.read_excel(BytesIO(contents),engine='openpyxl')
        else:
            raise ValueError("Unsupported file type. Only Excel and CSV are supported.")

    def replace_placeholders(self, message: str, row: pd.Series) -> str:
        customized_message = message
        for column_name in self.df.columns:
            placeholder = f"{{{column_name}}}"
            customized_message = re.sub(r"%7B", "{", customized_message, flags=re.IGNORECASE)
            customized_message = re.sub(r"%7D", "}", customized_message, flags=re.IGNORECASE)
            customized_message = customized_message.replace(placeholder, str(row[column_name]))
        return customized_message

    def send_email(self, to_address: str, body: str):
        try:
            with smtplib.SMTP_SSL(self.SMTP_SERVER, 465) as server:
                server.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
                msg = MIMEText(body)
                msg["Subject"] = self.subject
                msg["From"] = self.SMTP_USERNAME
                msg["To"] = to_address
                server.sendmail(self.SMTP_USERNAME, to_address, msg.as_string())
                
                print(f"Email sent to {to_address}")
        except Exception as e:
            print(f"Failed to send email to {to_address}: {e}")

    # async def send_bulk_emails(self):
    #     await self.read_file()

    #     if self.email_col not in self.df.columns:
    #         raise ValueError(f"'{self.email_col}' column not found in the file.")

    #     for _, row in self.df.iterrows():
    #         to_address = row[self.email_col]
    #         body = self.replace_placeholders(self.email_message, row)
    #         self.send_email(to_address, body)


    async def send_bulk_emails(self):
        await self.read_file()

        if self.email_col not in self.df.columns:
            raise ValueError(f"'{self.email_col}' column not found in the file.")

        try:
            with smtplib.SMTP_SSL(self.SMTP_SERVER, 465) as server:
                server.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)

                for _, row in self.df.iterrows():
                    to_address = row[self.email_col]
                    if not isinstance(to_address, str) or to_address.strip() == "" or to_address.lower() == "nan":
                        print(f"Skipping invalid email: {to_address}")
                        continue

                    body = self.replace_placeholders(self.email_message, row)
                    msg = MIMEText(body)
                    msg["Subject"] = self.subject
                    msg["From"] = self.SMTP_USERNAME
                    msg["To"] = to_address
                    server.sendmail(self.SMTP_USERNAME, to_address, msg.as_string())
                    print(f"Email sent to {to_address}")

        except Exception as e:
            print(f"Error sending emails: {e}")
