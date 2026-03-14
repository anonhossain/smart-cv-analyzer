```mermaid

classDiagram
    class BaseCVProcessor {
        +Config config
        +extract_text_from_pdf(file_path) String
        +load_job_description(file_path) String
        +process_resume(pdf_text, jd_text) JSON
    }

    class CVRanker {
        +rank_cvs(results_list) List
    }

    class QuestionGenerator {
        +generate_questions(analysis_data) String
        +save_to_disk(filename, content) bool
    }

    BaseCVProcessor <|-- CVRanker : inherits
    BaseCVProcessor <|-- QuestionGenerator : inherits
