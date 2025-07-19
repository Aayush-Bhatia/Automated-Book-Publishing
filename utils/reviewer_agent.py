
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  

def reviewer_agent(text):
    
    prompt = f"""
You are a professional book reviewer. Carefully read the following chapter content,
and provide improved or clearer rephrasing if needed, while preserving the meaning, tone, and flow.

If the content is already good, respond with "-- Looks good to go!".
Otherwise, provide your improved version below.

--- Content Start :
{text}
: Content End ---

Respond below:
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"-- Error in reviewer_agent: {str(e)}"
