from bellatrix.dmc.dmcr_client import DmcrRestClient
from bellatrix.dmc.dmc_client import DmcRestClient
from bellatrix.dmc.config import DmcrSettings, DmcSettings
from bellatrix.dmc.enums import DmcDocumentSource
from app.orion.services.tenant_service import get_dmcr_credentials_for_tenant, get_dmc_credentials_for_tenant

def make_dmcr_client(settings, tenant_id):
    creds = get_dmcr_credentials_for_tenant(tenant_id)
    config = settings.dmcr  # DmcrSettings instance
    return DmcrRestClient(config, creds["fid"], creds["password"])

def make_dmc_client(settings, tenant_id, token_manager):
    creds = get_dmc_credentials_for_tenant(tenant_id)
    config = settings.dmc  # DmcSettings instance
    return DmcRestClient(config, creds["client_id"], creds["client_secret"], token_manager) 