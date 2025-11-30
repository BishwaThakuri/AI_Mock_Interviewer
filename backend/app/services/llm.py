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
    
def grade_answer(question: str, user_answer: str):
    system_prompt = f"""
    You are a Senior Technical Interviewer.
    
    Question Asked: "{question}"
    Candidate's Answer (Transcribed via Speech-to-Text): "{user_answer}"
    
    **GRADING INSTRUCTIONS:**
    1. The candidate's answer was transcribed from audio. **Ignore minor phonetic errors** (e.g., "Java Script" vs "JavaScript", "Sequel" vs "SQL", "Liquid" vs "Eloquent").
    2. Focus on the **technical accuracy** and the **logic** of the answer.
    3. If the user makes a valid point but uses the wrong pronunciation/transcription, give them credit.
    
    Task:
    1. Grade the answer on a scale of 1-10.
    2. Provide 1-2 sentences of specific feedback.
    
    OUTPUT FORMAT (JSON ONLY):
    {{"score": 7, "feedback": "Feedback text here."}}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )
        
        response = chat_completion.choices[0].message.content
        
        # Simple JSON extraction
        start = response.find('{')
        end = response.rfind('}') + 1
        return json.loads(response[start:end])
        
    except Exception as e:
        print(f"Grading Error: {e}")
        return {"score": 0, "feedback": "Error grading answer."}