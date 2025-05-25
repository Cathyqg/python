from .base import BaseDocumentClient

class DMCClient(BaseDocumentClient):
    def __init__(self, config, client_id, client_secret, token_manager):
        super().__init__(config.hostname)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_manager = token_manager
        self.config = config

    async def _headers(self):
        token = await self.token_manager.get_token()
        return {
            "Authorization": f"Bearer {token.access_token}",
            "X-DMC-Apic-Header": self.config.x_dmc_apic_header,
            "X-DMC-Authentication": self.config.x_dmc_authentication,
        }

    async def download_document(self, document_id: str):
        url = f"{self.base_url}/restapi/v1/documents/{document_id}/coredoc/image"
        return await self.get(url, await self._headers())

    async def search_documents(self, search_body: dict):
        url = f"{self.base_url}/restapi/v1/search"
        return await self.post(url, await self._headers(), search_body) 