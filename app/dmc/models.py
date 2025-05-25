from pydantic import BaseModel
from typing import List

class DocumentRequest(BaseModel):
    id: str
    source: str  # or use DocumentSource enum

class DocumentSearchCriteria(BaseModel):
    key: str
    value: str
    condition: str = "equals" 