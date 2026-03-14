```mermaid
classDiagram
    %% Inheritance for AI Logic
    class BaseCVProcessor {
        +Config config
        +extract_text_from_pdf(file_path) String
        +load_job_description(file_path) String
        +process_resume(pdf_text, jd_text) JSON
    }

    class CVRanker {
        +rank_cvs(results_list) List
        +get_top_candidates(n) List
    }

    class QuestionGenerator {
        +generate_questions(analysis_data) String
        +save_to_disk(filename, content) bool
    }

    %% Communication Service
    class EmailSender {
        +String SMTP_SERVER
        +String subject
        +UploadFile file
        +read_file() async
        +replace_placeholders(message, row) String
        +send_bulk_emails() async
    }

    %% Relationships
    BaseCVProcessor <|-- CVRanker : Inheritance
    BaseCVProcessor <|-- QuestionGenerator : Inheritance
    CVRanker ..> EmailSender : Uses for notification
