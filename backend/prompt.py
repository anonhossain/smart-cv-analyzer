def candidate_match_prompt(job_desc, resume_text):
    return f"""
        You are an expert in the field of HR. 
        You have been asked to evaluate a candidate for a job position. The job description and the resume of the candidate are provided below. 
        You will first show the percentage match between the job description and CV in one line 
        write the main key skills and project missing from the CV for that job write it in short points. 
        Then create viva questions that could be asked based on the skills, job role, previous experience, and projects mentioned in the CV. Also, generate technical questions from CV projects and experience.

        Job Description:
        {job_desc}

        Resume:
        {resume_text}
        """

def hr_match_prompt(job_desc, resume_text):
    return f"""
            You are an expert in the field of HR. 
            You have been asked to evaluate a candidate for a job position. 
            The job description and the resume of the candidate are provided below. 
            
            Your task is to show the percentage match between the job description and CV in one line. 
            Just write the number without using %.
            Job Description:
            {job_desc}

            Resume:
            {resume_text}
            """
def generate_questions_prompt(job_desc, resume_text):
    return f"""
                You are a Highly Expert HR. Your main task is to go through the job description throughly. 
                Read that nicely and understand that nicely. 
                Then go through the resume of the candidate. 
                Read that nicely and understand that nicely. 
                Then you have to generate the questions that could be asked based on the skills, job role, previous experience, and projects mentioned in the CV.
                Also, generate technical questions from CV projects and experience. T
                he Question must be of high Standard and should be related to the job role and the skills mentioned in the CV. 
                Also ask some Advance level questions based on Skills and project which relate to the job description. 
                No need to ask general questions. The total number question will be between 10-15

                Job Description:
                {job_desc}

                Resume:
                {resume_text}
                """