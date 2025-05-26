from pydantic import BaseModel
from typing import List, Optional
from bellatrix.dmc.enums import DmcDocumentSource

class DmcDocumentRequest(BaseModel):
    id: str
    source: DmcDocumentSource

class DmcDocumentImportResult(BaseModel):
    id: str
    status: str
    data: Optional[dict] = None
    error: Optional[str] = None

class DmcDocumentImportResponse(BaseModel):
    results: List[DmcDocumentImportResult]

class DmcDocumentSearchCriteria(BaseModel):
    key: str
    value: str
    condition: str = "equals"

class DmcDocumentSearchRequest(BaseModel):
    criteria: List[DmcDocumentSearchCriteria]
    source: DmcDocumentSource

class DmcDocumentSearchResponse(BaseModel):
    results: List[dict] 