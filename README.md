# 🧠 AI-Powered Recruitment Assistant

CV Tutor is a smart AI-based web application that enhances job applications for candidates and streamlines the recruitment process for HR teams. It compares resumes with job descriptions, suggests improvements, and automates key hiring workflows.

---

## ✨ Features

### 👨‍💼 For Candidates:

- 🔢 **Percentage Match**  
  Calculates how closely the resume aligns with the provided job description.

- 🔍 **Missing Skills Detection**  
  Identifies essential skills listed in the job description but not found in the resume.

- 💡 **Improvement Suggestions**  
  Provides actionable advice on how to tailor the resume to better fit the job description.

- ❓ **Question Generation**  
  Generates potential interview questions based on both the resume and job description to help the candidate prepare.

---
![Test Resume Result](https://github.com/anonhossain/cv_project/blob/main/screenshots/12%20Test%20resume%20result.PNG)

### 🧑‍💻 For HR Teams:

- 📊 **CV Sorting by Match %**  
  Automatically sorts multiple resumes against a single job description based on compatibility scores.

![Sort CV](https://github.com/anonhossain/cv_project/blob/main/screenshots/5.%20Analyze%20CV.PNG)

- 📥 **Resume Data Extraction**  
  Extracts candidate details like:
  - Full Name
  - Email
  - Phone Number
  - Reference Emails & Phone Numbers  
  Saves this information in an organized Excel sheet.

![Extract Info](https://github.com/anonhossain/cv_project/blob/main/screenshots/6.Extract%20info.PNG)

- 📧 **Email Automation**  
  Automatically sends emails to selected candidates using customizable templates.

![Send Email](https://github.com/anonhossain/cv_project/blob/main/screenshots/9.2.PNG)
----
![Received Email](https://github.com/anonhossain/cv_project/blob/main/screenshots/9.3.PNG)

- 📄 **Interview Question Generation**  
  Generates a tailored set of viva questions for each candidate and saves them in a `.docx` file.

![Generate Multiple Questions](https://github.com/anonhossain/cv_project/blob/main/screenshots/11%20Generate%20Question%20Output.PNG)
----
![Each Question File](https://github.com/anonhossain/cv_project/blob/main/screenshots/7.Generate%20Q.PNG)

## 🖼️ Other Screenshots

### 📌 Landing Page
![Landing Page](https://github.com/anonhossain/cv_project/blob/main/screenshots/1.PNG)

### 📌 Login and Signup
![Login](https://github.com/anonhossain/cv_project/blob/main/screenshots/3.PNG)

### 📌 Admin Panel
![Login](https://github.com/anonhossain/cv_project/blob/main/screenshots/Admin%20credential%20change.PNG)

### 📌 Dashboard & Main Features
![Dashboard](https://github.com/anonhossain/cv_project/blob/main/screenshots/4%20hrbody.PNG)

---

## 🚀 Tech Stack

- **Frontend:** `HTML`, `CSS`, `JavaScript`
- **Backend:** `Python`, `FastAPI`
- **AI/NLP:** `Gemini`, `Redex`
- **File Handling:** `python-docx`, `openpyxl`, `pdfplumber`
- **Automation:** `SMTP`, `Email Templates`

---

## 🛠️ How to Use This Repository

Follow these steps to get the AI-Powered Recruitment Assistant running locally:

### 1. Clone the repository**  
```bash
git clone https://github.com/anonhossain/smart-cv-analyzer.git
cd smart-cv-analyzer
```
### 2. Create a virtual environment 

```bash
python3 -m venv .venv
```
**Note:** Use `python` instead of `python3` based on your system.

### 3. Activate the virtual environment 
- **On Windows:**

```bash
.venv\Scripts\activate
```

- **On MacOs/Linux:**

```bash
source .venv/bin/activate
```
  
### 4. Install Dependencies

```bash
pip install -r requirements.txt
```
### 5. Create a `.env` file in the project root and add your API key(s)
- Get your Gemini API key here (or your preferred AI service).
- Example `.env` content:
  
  ``` env
  CANDIDATE_CV_FILE=..\\uploads\\candidate\\cv\\resume.pdf
  CANDIDATE_JD_FILE=..\\uploads\\candidate\\jd\\jd.txt

  HR_CV_FILE=./uploads/hr/cv/
  HR_JD_FILE=./uploads/hr/jd/

  OUTPUT_DIRECTORY=./output

  SMTP_SERVER="smtp.gmail.com"
  SMTP_USERNAME="Your_Email"
  SMTP_PASSWORD="App Password"
  PORT=465

  GOOGLE_API_KEY = "Your_API_Key"
  MODEL = "Your_Prefered_Model"
  
  ```

### 6. Install Xampp MySQL
[Download Xampp](https://www.apachefriends.org/download.html)

### 7. Create Database and table for the project
**Create database:**

```sql
CREATE DATABASE smart_resume_analyzer;
USE smart_resume_analyzer;
```
**Create table:**
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 8. Run the application

```bash
uvicorn main:app --reload
```

### 9. Access the App
**Open your browser and go to:**

```cpp
http://127.0.0.1:8000
```

Now you’re ready to start uploading resumes and job descriptions to analyze, generate questions, and automate email workflows.

