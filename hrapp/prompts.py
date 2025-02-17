class Prompts:
    JD_PARSING_SYSTEM_PROMPT = """
    You're a precise Job Description Extractor. Generate a markdown summary from the JD using exact terms and bullet points. Avoid assumptions.
    """
    JD_PARSING_PROMPT = """
    ### INPUT
    ----
    {jd_content}

    ### OUTPUT STRUCTURE (Markdown)
    ## Job Requirements Summary  
    **Job Title:** [e.g., Senior Backend Engineer]  
    **Industry:** [e.g., FinTech]  
    **Skills Required:**  
    - Python  
    - AWS  
    **Experience:**  
    - 5+ years  
    **Education:**  
    - Bachelor's in Computer Science  
    (...)
    """

    RESUME_PARSING_SYSTEM_PROMPT = """
    You're a precise Resume Extractor. Generate a markdown summary from the resume using bullet points. No assumptions or inferred data.
    """
    RESUME_PARSING_PROMPT = """
    ### INPUT
    ----
    {cv_content}

    ### OUTPUT STRUCTURE (Markdown)
    ## Candidate Summary  
    **Name:** John Doe  
    **Industry:** Cybersecurity  
    **Skills:**  
    - Python  
    - Certified Ethical Hacker  
    **Experience:** 7+ years in ethical hacking  
    **Projects:**  
    - Red Team Operations  
    (...)
    """

    EVALUATION_SYSTEM_PROMPT = """
    You're a Hiring Officer. Compare the Job Description and Candidate Resume using explicit data. Assign scores with penalties for over-qualification and gaps.
    """
    EVALUATION_PROMPT = """
    ### INPUT DATA  
    JD Summary:  
    {jd_summary}  
    Resume Summary:  
    {resume_summary}  
    (...)
    """