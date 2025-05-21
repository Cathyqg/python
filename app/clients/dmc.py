from app.clients.base import BaseDocumentClient
from app.settings import settings

class DMCClient(BaseDocumentClient):
    def __init__(self):
        super().__init__(settings.dmc_base_url)

    async def download_document(self, document_id: str):
        headers = {"Authorization": f"Bearer {self.get_token()}"}
        return await super().download_document(document_id, headers)

    async def get_metadata(self, document_id: str):
        headers = {"Authorization": f"Bearer {self.get_token()}"}
        return await super().get_metadata(document_id, headers)

    def get_token(self):
        # TODO: Implement DMC-specific token logic
        return "dmc-token" 