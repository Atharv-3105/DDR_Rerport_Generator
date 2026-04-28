from groq import Groq
import os 
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class DDRGenerator:
    def __init__(self, merged_data):
        self.data = merged_data
        
    
    def generate_report(self):
        prompt = self._build_prompt()
        
        response = client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages = [
                {
                    "role":"system",
                    "content": "You are a professional civil engineer creating a client-friendly diagnostic report."
                },
                {
                    "role":"user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    
    def _build_prompt(self):
        return f"""
    Generate a Detailed Diagnostic Report (DDR) based ONLY on the provided data.

    STRICT RULES:
    - Use simple, clear, client-friendly language
    - Do NOT use technical jargon
    - Do NOT invent or assume information
    - ONLY use facts present in the data
    - If any detail is missing → write "Not Available"
    - Do NOT leave any field empty
    - Do NOT use generic phrases like "further investigation required"
    - Do NOT add new observations (e.g., smell, stains, etc.)
    - Ensure the report sounds like a real professional inspection document

    DATA:
    Area Summary:
    {self.data["area_summary"]}

    Severity:
    {self.data["severity"]}

    Thermal Signals:
    {self.data["thermal_signals"]}

    ---

    OUTPUT FORMAT:

    1. Property Issue Summary  
    → Summarize key issues in 3–5 bullet points  
    → Mention affected areas and major issue types  

    2. Area-wise Observations  
    → For each area:
    - Issue
    - What was observed (ONLY from data or "Not Available")
    - Where (location detail or "Not Available")
    - Supporting detail (page reference if available)

    3. Probable Root Cause  
    → Clearly connect issues:
    - Dampness → tile gaps or plumbing issues  
    - Leakage → bathroom or structural source  
    - Thermal anomaly → supports moisture presence  
    → Be specific and avoid vague wording  

    4. Severity Assessment (WITH REASONING)  
    → For each area:
    - Severity (High / Medium / Low)
    - Reason based on:
        - number of issues
        - type of issues:
        • Leakage / Seepage → High impact  
        • Dampness → Medium impact  
        • Tile gaps / hollowness → Lower impact  

    5. Recommended Actions  
    → Provide practical and actionable steps:
    - Example: "Seal tile joints using waterproof grout"
    - Example: "Fix plumbing leaks in bathroom"
    → Avoid vague advice  

    6. Additional Notes  
    → Include:
    - Thermal analysis insight (mention temperature variation clearly)
    - Any limitations in the data  

    7. Missing or Unclear Information  
    → Explicitly list:
    - Missing descriptions
    - Missing locations
    - Any unclear findings  

    ---

    IMPORTANT:
    - Do NOT repeat the same sentences
    - Do NOT output placeholders
    - Do NOT include invalid issue labels like "Issue"
    - Ensure all sections are complete and cleanly formatted

    Generate the report now:
    """