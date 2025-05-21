import httpx
from app.clients.exceptions import AccessDeniedException, DocumentNotFoundException, UpstreamServiceException

class BaseDocumentClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def download_document(self, document_id: str, headers: dict):
        url = f"{self.base_url}/{document_id}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
            except Exception as e:
                raise UpstreamServiceException(str(e))
            if response.status_code == 403:
                raise AccessDeniedException(f"Access denied for document {document_id}")
            if response.status_code == 404:
                raise DocumentNotFoundException(f"Document {document_id} not found.")
            if response.status_code != 200:
                raise UpstreamServiceException(f"Error: {response.status_code}")
            filename = document_id  # Or parse from response if needed
            return response.content, filename

    async def get_metadata(self, document_id: str, headers: dict):
        url = f"{self.base_url}/metadata/{document_id}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
            except Exception as e:
                raise UpstreamServiceException(str(e))
            if response.status_code == 403:
                raise AccessDeniedException(f"Access denied for document {document_id}")
            if response.status_code == 404:
                raise DocumentNotFoundException(f"Document {document_id} not found.")
            if response.status_code != 200:
                raise UpstreamServiceException(f"Error: {response.status_code}")
            return response.json() 