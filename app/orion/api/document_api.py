from fastapi import APIRouter, Depends, HTTPException, Body
from bellatrix.dmc.enums import DmcDocumentSource
from bellatrix.dmc.models import DmcDocumentRequest
from app.orion.orion import make_dmcr_client, make_dmc_client
from app.orion.services.tenant_service import get_current_tenant_id

router = APIRouter()

@router.post("/documents/import")
async def import_documents(
    requests: list[DmcDocumentRequest] = Body(...),
    source: DmcDocumentSource = Body(...),
    tenant_id: str = Depends(get_current_tenant_id),
    settings = Depends(lambda: None),  # Replace with your settings DI
    token_manager = Depends(lambda: None)  # Replace with your token manager DI
):
    if source == DmcDocumentSource.dmcr:
        client = make_dmcr_client(settings, tenant_id)
    elif source == DmcDocumentSource.dmc:
        client = make_dmc_client(settings, tenant_id, token_manager)
    else:
        raise HTTPException(400, "Invalid source")
    results = []
    for req in requests:
        try:
            doc = await client.download_document(req.id)
            results.append({"id": req.id, "status": "success", "data": doc})
        except Exception as e:
            results.append({"id": req.id, "status": "error", "error": str(e)})
    return results

@router.post("/documents/search")
async def search_documents(
    search_body: dict = Body(...),
    source: DmcDocumentSource = Body(...),
    tenant_id: str = Depends(get_current_tenant_id),
    settings = Depends(lambda: None),  # Replace with your settings DI
    token_manager = Depends(lambda: None)  # Replace with your token manager DI
):
    if source == DmcDocumentSource.dmcr:
        client = make_dmcr_client(settings, tenant_id)
    elif source == DmcDocumentSource.dmc:
        client = make_dmc_client(settings, tenant_id, token_manager)
    else:
        raise HTTPException(400, "Invalid source")
    try:
        result = await client.search_documents(search_body)
        return result.json()
    except Exception as e:
        raise HTTPException(500, str(e)) 