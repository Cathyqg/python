from fastapi import APIRouter, HTTPException, Body
from app.clients.dmcr import DMCRClient
from app.clients.exceptions import AccessDeniedException, DocumentNotFoundException, UpstreamServiceException
from app.services.s3 import S3Service
from app.services.embedding import EmbeddingService
from app.models.document import DocumentMetadata, UploadResponse, UploadBatchResponse, UploadResult
from typing import List, Union

router = APIRouter(prefix="/files", tags=["files"])

dmcr_client = DMCRClient()
s3_service = S3Service()
embedding_service = EmbeddingService()

# In-memory metadata store for demo
metadata_store = {}

@router.post("/upload", response_model=UploadBatchResponse)
async def upload_files(documentIds: Union[str, List[str]] = Body(..., embed=True)):
    if isinstance(documentIds, str):
        documentIds = [documentIds]
    results = []
    for doc_id in documentIds:
        try:
            file_content, filename = await dmcr_client.download_document(doc_id)
            s3_url = s3_service.upload_file(filename, file_content)
            embedding = embedding_service.generate_embedding(file_content)
            file_id = doc_id
            metadata = DocumentMetadata(
                file_id=file_id,
                filename=filename,
                s3_url=s3_url,
                embedding=embedding,
            )
            metadata_store[file_id] = metadata
            results.append(UploadResult(documentId=doc_id, status="success", metadata=metadata))
        except AccessDeniedException:
            results.append(UploadResult(documentId=doc_id, status="forbidden", error="Access denied"))
        except DocumentNotFoundException:
            results.append(UploadResult(documentId=doc_id, status="not_found", error="Document not found"))
        except UpstreamServiceException as e:
            results.append(UploadResult(documentId=doc_id, status="upstream_error", error=str(e)))
        except Exception as e:
            results.append(UploadResult(documentId=doc_id, status="error", error=str(e)))
    return UploadBatchResponse(results=results)

@router.get("/{file_id}/metadata", response_model=DocumentMetadata)
async def get_metadata(file_id: str):
    metadata = metadata_store.get(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Metadata not found.")
    return metadata 