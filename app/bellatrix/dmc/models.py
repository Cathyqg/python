from pydantic import BaseModel
from typing import List

class DmcDocumentRequest(BaseModel):
    id: str
    source: str  # or use DmcDocumentSource enum

class DmcDocumentSearchCriteria(BaseModel):
    key: str
    value: str
    condition: str = "equals" 