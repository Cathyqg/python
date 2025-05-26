from fastapi import APIRouter, Depends, HTTPException, Body
from bellatrix.dmc.models import (
    DmcDocumentRequest,
    DmcDocumentImportResponse,
    DmcDocumentImportResult,
    DmcDocumentSearchRequest,
    DmcDocumentSearchResponse,
)
from app.orion.orion import make_dmcr_client, make_dmc_client
from app.orion.services.tenant_service import get_current_tenant_id

router = APIRouter()

@router.post("/documents/import", response_model=DmcDocumentImportResponse)
async def import_documents(
    requests: list[DmcDocumentRequest] = Body(...),
    tenant_id: str = Depends(get_current_tenant_id),
    settings = Depends(lambda: None),  # Replace with your settings DI
    token_manager = Depends(lambda: None)  # Replace with your token manager DI
):
    results = []
    for req in requests:
        if req.source == "dmcr":
            client = make_dmcr_client(settings, tenant_id)
        elif req.source == "dmc":
            client = make_dmc_client(settings, tenant_id, token_manager)
        else:
            results.append(DmcDocumentImportResult(id=req.id, status="error", error="Invalid source"))
            continue
        try:
            doc = await client.download_document(req.id)
            results.append(DmcDocumentImportResult(id=req.id, status="success", data=doc))
        except Exception as e:
            results.append(DmcDocumentImportResult(id=req.id, status="error", error=str(e)))
    return DmcDocumentImportResponse(results=results)

@router.post("/documents/search", response_model=DmcDocumentSearchResponse)
async def search_documents(
    request: DmcDocumentSearchRequest = Body(...),
    tenant_id: str = Depends(get_current_tenant_id),
    settings = Depends(lambda: None),  # Replace with your settings DI
    token_manager = Depends(lambda: None)  # Replace with your token manager DI
):
    if request.source == "dmcr":
        client = make_dmcr_client(settings, tenant_id)
    elif request.source == "dmc":
        client = make_dmc_client(settings, tenant_id, token_manager)
    else:
        raise HTTPException(400, "Invalid source")
    try:
        result = await client.search_documents([c.dict() for c in request.criteria])
        return DmcDocumentSearchResponse(results=result.json())
    except Exception as e:
        raise HTTPException(500, str(e)) 