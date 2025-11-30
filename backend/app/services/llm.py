import os
import json
from groq import Groq
from dotenv import load_dotenv

# Force load .env from the backend folder
# This ensures it finds the key even if you run from a different folder
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(base_dir, ".env"))

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_questions(resume_text: str, job_role: str = "Software Engineer"):
    # --- SAFETY CHECK: Handle empty text ---
    if not resume_text:
        return ["Error: Resume text is empty. Please re-upload the resume."]

    system_prompt = f"""
    You are a Senior Technical Interviewer for a {job_role} position.
    I will provide you with a candidate's resume. 
    
    Your goal is to generate 3 challenging technical questions and 1 behavioral question 
    based SPECIFICALLY on the skills and projects listed in the resume.
    
    Resume Context:
    {resume_text[:4000]} 
    
    OUTPUT FORMAT:
    Return ONLY a raw JSON list of strings. Do not add markdown formatting like ```json.
    Example: ["Question 1", "Question 2", "Question 3", "Question 4"]
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )

        response_content = chat_completion.choices[0].message.content
        
        # Clean the response to ensure it's valid JSON
        start_index = response_content.find('[')
        end_index = response_content.rfind(']') + 1
        
        if start_index != -1 and end_index != -1:
            clean_json = response_content[start_index:end_index]
            questions = json.loads(clean_json)
            return questions
        else:
            return ["Tell me about your experience with Python.", "Describe a challenging project."]

    except Exception as e:
        print(f"AI Error: {e}")
        return ["Error generating questions. Please check the backend logs."]