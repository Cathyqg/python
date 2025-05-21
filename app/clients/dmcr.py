import httpx
from app.settings import settings
from app.clients.exceptions import AccessDeniedException, DocumentNotFoundException, UpstreamServiceException

class DMCRClient:
    def __init__(self):
        self.base_url = settings.dmcr_base_url
        self.fid = settings.dmcr_fid
        self.password = settings.dmcr_password
        self.document_map = settings.dmcr_document_map or {}

    def get_document_url(self, document_id: str) -> str:
        url = self.document_map.get(document_id)
        if not url:
            raise DocumentNotFoundException(f"Document {document_id} not found.")
        return url

    async def download_document(self, document_id: str):
        url = self.get_document_url(document_id)
        headers = {"fid": self.fid, "password": self.password}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/{url}", headers=headers)
            except Exception as e:
                raise UpstreamServiceException(str(e))
            if response.status_code == 403:
                raise AccessDeniedException(f"Access denied for document {document_id}")
            if response.status_code == 404:
                raise DocumentNotFoundException(f"Document {document_id} not found.")
            if response.status_code != 200:
                raise UpstreamServiceException(f"DMCR error: {response.status_code}")
            filename = url.split("/")[-1]
            return response.content, filename 