import json 
import os 
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
#Initialize the GROQ client 
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

class LLMExtractor:
    def __init__(self, source_type):
        self.source_type = source_type
    
    #===========Function to extract data from the Page============= 
    def extract_from_page(self, pages_batch):
        
        #Get combined text of batched_pages
        combined_text = ""
        
        for page in pages_batch:
            combined_text += f"\n --PAGE {page['page_number']} ---\n"
            combined_text += page["text"][:1500] 
        
        #Get the Prompt for correct extraction
        prompt = self.build_prompt(combined_text)
        
        #Reponse from the LLM
        response = client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages = [
                {
                    "role":"system",
                    "content":"You are a strict information extraction system. Output ONLY valid JSON."
                },
                {
                    "role":"user",
                    "content": prompt
                }
            ], temperature=0
        )
        
        content = response.choices[0].message.content
        
        return self._safe_json_parse(content)
    
    #========Function to safely extract the JSON from LLM Response==============
    def _safe_json_parse(self, content):
        try:
            #Return safe JSON response
            return json.loads(content)
        except:
            start = content.find("{")
            end = content.rfind("}") + 1
            
            if start != -1 and end != -1:
                try:
                    return json.loads(content[start:end])
                except:
                    pass 
            
            return {"observations": []}
        
    #=========Function to build the Prompt to give to LLM=================
    def build_prompt(self, text):
        return f"""
    Extract structured observations from the given page.

        STRICT RULES:
        - Output ONLY valid JSON
        - Do NOT include explanations
        - Do NOT hallucinate
        - If no observation → return empty list
        - Be concise and accurate
        - Extract page_number frmo markers like: --- PAGE X ---

        SOURCE: {self.source_type}

        OUTPUT FORMAT:
        {{
        "observations": [
            {{
            "area": "",
            "sub_area": "",
            "issue_type": "",
            "description": "",
            "location_detail": "",
            "severity_hint": "low | medium | high | unknown",
            "possible_cause": "",
            "source": "{self.source_type}",
            "evidence": {{
                "text_excerpt": "",
                "page_number": ""
            }}
            }}
        ]
        }}

        PAGE TEXT:
        {text}
    """
        
    
        