import io
import json
import traceback
import pandas as pd
from fastapi import HTTPException
from google import genai
from google.genai import types
from backend.config import settings

class LeadPipelineService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            print("⚠️ WARNING: GEMINI_API_KEY is missing or empty! Check your .env file.")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.MODEL_NAME

    def parse_file(self, contents: bytes, filename: str) -> pd.DataFrame:
        try:
            if filename.endswith('.csv'):
                return pd.read_csv(io.BytesIO(contents))
            elif filename.endswith(('.xls', '.xlsx')):
                return pd.read_excel(io.BytesIO(contents))
            else:
                raise HTTPException(status_code=400, detail="Invalid file format. Upload CSV or Excel.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

    def evaluate_lead_batch(self, batch_data: list, company_context: str, custom_properties: list) -> list:
        properties_instructions = "\n".join([f"- {prop}: (Required output property)" for prop in custom_properties])
        
        system_instruction = f"""
        You are an elite B2B Sales & Lead Qualification AI. 
        Company Context & Ideal Customer Profile (ICP) Rules:
        {company_context}

        Task: Analyze each customer row in the provided batch list. 
        You MUST return a valid JSON object with a single key "results" containing an array of objects.
        Each object in the array MUST include:
        - "row_index": matching the exact row_index provided in the input item.
        - Every one of these requested custom properties:
        {properties_instructions}
        
        Ensure the output is strictly valid JSON format without markdown code blocks if possible.
        """

        prompt = f"Batch Customer Data Rows (Chunk of up to 40):\n{json.dumps(batch_data, default=str)}"

        try:
            # Using response_mime_type="application/json" without response_schema 
            # to fully support dynamic custom properties without triggering Pydantic additionalProperties errors.
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            
            text_response = response.text.strip()
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
                
            data = json.loads(text_response.strip())
            return data.get("results", [])
        except Exception as e:
            print(f"❌ GEMINI BATCH API ERROR: {str(e)}")
            traceback.print_exc()
            # Return graceful fallback error state for this batch
            fallback_res = {}
            for prop in custom_properties:
                fallback_res[prop] = "N/A"
            return [ {**item, "reason": f"AI Error: {str(e)[:80]}", **fallback_res} for item in batch_data ]

    def dataframe_to_csv_stream(self, df: pd.DataFrame) -> io.BytesIO:
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return output

pipeline_service = LeadPipelineService()