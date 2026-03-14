```mermaid
classDiagram
    %% Core AI Logic (The Foundation)
    class BaseCVProcessor {
        +Config config
        +extract_text_from_pdf(file) String
        +load_job_description(file) String
        +process_resume(pdf_text, jd_text) JSON
    }

    %% Regular User Logic (Inherits from Base)
    class RegularCandidate {
        +get_percentage_match(cv_text, jd_text) String
        +get_viva_suggestions(cv_text, jd_text) String
        +get_project_suggestion(cv_text, jd_text) String
    }

    %% HR Logic (Inherits from Base)
    class HRPerson {
        +cv_ranker(cv_list, jd_text) List
        +get_top_candidates(n) List
        +generate_viva_questions(cv_text, jd_text) String
    }

    %% Document Utility (Inherits from Base)
    class QuestionGenerator {
        +generate_questions(analysis_data) String
        +save_to_disk(filename, content) bool
    }

    %% External Communication Service
    class EmailSender {

        +String SMTP_SERVER
        +String SMTP_USERNAME
        +String SMTP_PASSWORD
        +String subject
        +UploadFile file
        +String email_col
        +String email_message
        +read_file() async
        +replace_placeholders(message, row) String
        +send_bulk_emails() async
    }

    %% Connections
    BaseCVProcessor <|-- RegularCandidate : Inherits
    BaseCVProcessor <|-- HRPerson : Inherits
    BaseCVProcessor <|-- QuestionGenerator : Inherits

    HRPerson ..> EmailSender : Uses for Bulk Notifications
    HRPerson ..> QuestionGenerator : Uses for PDF Export
