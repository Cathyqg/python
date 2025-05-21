from fastapi import APIRouter, HTTPException, Body
from app.clients.dmcr import DMCRClient
from app.clients.dmc import DMCClient
from app.clients.exceptions import AccessDeniedException, DocumentNotFoundException, UpstreamServiceException
from app.services.s3 import S3Service
from app.services.embedding import EmbeddingService
from app.models.document import DocumentMetadata, UploadBatchResponse, UploadResult, DocumentRequest
from app.models.enums import DocumentSource
from typing import List

router = APIRouter(prefix="/files", tags=["files"])

dmcr_client = DMCRClient()
dmc_client = DMCClient()
PROVIDERS = {
    DocumentSource.dmcr: dmcr_client,
    DocumentSource.dmc: dmc_client,
}
s3_service = S3Service()
embedding_service = EmbeddingService()

# In-memory metadata store for demo
metadata_store = {}

@router.post("/upload", response_model=UploadBatchResponse)
async def upload_files(documents: List[DocumentRequest] = Body(..., embed=True)):
    results = []
    for doc in documents:
        provider = PROVIDERS.get(doc.source)
        if not provider:
            results.append(UploadResult(documentId=doc.id, status="invalid_source", error=f"Unknown source: {doc.source}"))
            continue
        try:
            file_content, filename = await provider.download_document(doc.id)
            s3_url = s3_service.upload_file(filename, file_content)
            embedding = embedding_service.generate_embedding(file_content)
            file_id = doc.id
            metadata = DocumentMetadata(
                file_id=file_id,
                filename=filename,
                s3_url=s3_url,
                embedding=embedding,
            )
            metadata_store[file_id] = metadata
            results.append(UploadResult(documentId=doc.id, status="success", metadata=metadata))
        except AccessDeniedException:
            results.append(UploadResult(documentId=doc.id, status="forbidden", error="Access denied"))
        except DocumentNotFoundException:
            results.append(UploadResult(documentId=doc.id, status="not_found", error="Document not found"))
        except UpstreamServiceException as e:
            results.append(UploadResult(documentId=doc.id, status="upstream_error", error=str(e)))
        except Exception as e:
            results.append(UploadResult(documentId=doc.id, status="error", error=str(e)))
    return UploadBatchResponse(results=results)

@router.get("/metadata/{source}/{file_id}")
async def get_metadata(source: DocumentSource, file_id: str):
    provider = PROVIDERS.get(source)
    if not provider:
        raise HTTPException(status_code=400, detail="Invalid source")
    try:
        metadata = await provider.get_metadata(file_id)
        return metadata
    except AccessDeniedException:
        raise HTTPException(status_code=403, detail="Access denied")
    except DocumentNotFoundException:
        raise HTTPException(status_code=404, detail="Metadata not found")
    except UpstreamServiceException as e:
        raise HTTPException(status_code=502, detail=str(e)) 