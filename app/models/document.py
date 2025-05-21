from pydantic import BaseModel
from typing import List, Optional

class DocumentMetadata(BaseModel):
    file_id: str
    filename: str
    s3_url: str
    embedding: List[float]

class UploadResult(BaseModel):
    documentId: str
    status: str
    metadata: Optional[DocumentMetadata] = None
    error: Optional[str] = None

class UploadBatchResponse(BaseModel):
    results: List[UploadResult]

class UploadResponse(BaseModel):
    metadata: DocumentMetadata 