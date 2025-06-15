import os
import dotenv
from groq import Groq # Import the Groq client

dotenv.load_dotenv()

# Initialize the Groq client
# Ensure GROQ_API_KEY is set in your environment variables or .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def is_relevant(job_desc, resume_text):
    """
    Determines if a job description is relevant to a given resume using Groq AI.

    Args:
        job_desc (str): The text of the job description.
        resume_text (str): The text of the resume.

    Returns:
        bool: True if the job is relevant, False otherwise.
    """
    prompt = f"""
Resume:
{resume_text}

Job Description:
{job_desc}

Is this job relevant to the user? Answer 'yes' or 'no' and explain.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192", # Using a common Groq model. You can choose others like "mixtral-8x7b-32768".
        messages=[{"role": "user", "content": prompt}],
        temperature=0 # Keep temperature low for deterministic answers
    )
    reply = response.choices[0].message.content.strip().lower()
    return reply.startswith("yes")

# Example Usage:
# if __name__ == "__main__":
#     sample_resume = """
#     John Doe
#     Software Engineer with 5 years experience in Python, JavaScript, and React.
#     """
#     sample_job_desc_relevant = """
#     Seeking a Senior Software Engineer skilled in Python and web development.
#     """
#     sample_job_desc_irrelevant = """
#     Looking for a Marketing Specialist with experience in SEO and content creation.
#     """

#     print(f"Is relevant (Software Engineer): {is_relevant_groq(sample_job_desc_relevant, sample_resume)}")
#     print(f"Is relevant (Marketing Specialist): {is_relevant_groq(sample_job_desc_irrelevant, sample_resume)}")