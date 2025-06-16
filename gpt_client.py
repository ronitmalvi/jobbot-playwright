# config.py
# Make sure to set your Groq API key in this file
# GROQ_API_KEY = "your_groq_api_key_here"
# LINKEDIN_EMAIL = "your_linkedin_email@example.com"
# LINKEDIN_PASSWORD = "your_linkedin_password"


import groq
from config import GROQ_API_KEY # Updated import for Groq API key

groq.api_key = GROQ_API_KEY # Using Groq API key

def ask_groq(prompt: str, model="mixtral-8x7b-32768", temp=0.2) -> str: # Renamed function to ask_groq and set a default Groq model
    """
    Sends a prompt to the Groq API and returns the generated response.

    Args:
        prompt (str): The prompt to send to the LLM.
        model (str): The model to use for generation (default: "mixtral-8x7b-32768").
        temp (float): The sampling temperature (default: 0.2).

    Returns:
        str: The generated text content.
    """
    client = groq.Groq(api_key=GROQ_API_KEY) # Initialize Groq client

    resp = client.chat.completions.create( # Using Groq's chat completions API
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
    )
    return resp.choices[0].message.content.strip()


