import httpx
from .exceptions import DmcAccessDeniedException, DmcDocumentNotFoundException, DmcUpstreamServiceException

class BaseDmcRestClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get(self, url: str, headers: dict):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 403:
                raise DmcAccessDeniedException()
            if response.status_code == 404:
                raise DmcDocumentNotFoundException()
            if response.status_code != 200:
                raise DmcUpstreamServiceException(f"Error: {response.status_code}")
            return response

    async def post(self, url: str, headers: dict, json: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=json)
            if response.status_code == 403:
                raise DmcAccessDeniedException()
            if response.status_code == 404:
                raise DmcDocumentNotFoundException()
            if response.status_code != 200:
                raise DmcUpstreamServiceException(f"Error: {response.status_code}")
            return response 