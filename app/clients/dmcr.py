from app.clients.base import BaseDocumentClient
from app.settings import settings
from app.clients.exceptions import AccessDeniedException, DocumentNotFoundException, UpstreamServiceException

class DMCRClient(BaseDocumentClient):
    def __init__(self):
        super().__init__(settings.dmcr_base_url)
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
        return await super().download_document(url, headers)

    async def download_document_from_url(self, url: str):
        headers = {"fid": self.fid, "password": self.password}
        return await super().download_document(url, headers)

    async def get_metadata(self, document_id: str):
        headers = {"fid": self.fid, "password": self.password}
        return await super().get_metadata(document_id, headers) 