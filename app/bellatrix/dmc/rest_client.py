from .base import BaseDmcRestClient

class DmcRestClient(BaseDmcRestClient):
    def __init__(self, config, client_id, client_secret, token_manager, is_dmc=False, soeid=None):
        super().__init__(config.hostname)
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_manager = token_manager
        self.config = config
        self.is_dmc = is_dmc
        self.soeid = soeid

    async def _headers(self):
        token = await self.token_manager.get_token()
        headers = {
            "Authorization": f"Bearer {token.access_token}",
            "X-DMC-Apic-Header": self.config.x_dmc_apic_header,
            "X-DMC-Authentication": self.config.x_dmc_authentication,
        }
        if self.is_dmc and self.soeid:
            headers["soeid"] = self.soeid
        return headers

    async def download_document(self, document_id: str):
        url = f"{self.base_url}/restapi/v1/documents/{document_id}/coredoc/image"
        return await self.get(url, await self._headers())

    async def search_documents(self, search_body: dict):
        url = f"{self.base_url}/restapi/v1/search"
        return await self.post(url, await self._headers(), search_body) 