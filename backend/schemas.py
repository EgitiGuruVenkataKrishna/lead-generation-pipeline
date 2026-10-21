from pydantic import BaseModel, Field
from typing import List, Dict, Any

class BatchLeadResponse(BaseModel):
    results: List[Dict[str, Any]] = Field(description="List of evaluated customer lead rows with requested custom properties.")