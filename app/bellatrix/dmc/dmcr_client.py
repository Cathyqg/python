from .base import BaseDmcRestClient

class DmcrRestClient(BaseDmcRestClient):
    def __init__(self, config, fid, password):
        super().__init__(config.hostname)
        self.fid = fid
        self.password = password
        self.config = config

    def _headers(self):
        return {
            "fid": self.fid,
            "password": self.password,
            "X-DMCR-Apic-Header": self.config.x_dmcr_apic_header,
            "X-DMCR-Authentication": self.config.x_dmcr_authentication,
        }

    async def download_document(self, document_id: str):
        url = f"{self.base_url}/restapi/v1/documents/{document_id}/coredoc/image"
        return await self.get(url, self._headers())

    async def search_documents(self, search_body: dict):
        url = f"{self.base_url}/restapi/v1/search"
        return await self.post(url, self._headers(), search_body) 