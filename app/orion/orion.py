from bellatrix.dmc.rest_client import DmcRestClient
from bellatrix.dmc.config import DmcrSettings, DmcSettings
from bellatrix.dmc.enums import DmcDocumentSource
from bellatrix.dmc.secret_utils import get_client_id, get_client_secret

def make_dmcr_client(settings, tenant_id, token_manager):
    client_id = get_client_id(tenant_id, "dmcr")
    client_secret = get_client_secret(tenant_id, "dmcr")
    config = settings.dmcr  # DmcrSettings instance
    return DmcRestClient(config, client_id, client_secret, token_manager, is_dmc=False)

def make_dmc_client(settings, tenant_id, token_manager, soeid):
    client_id = get_client_id(tenant_id, "dmc")
    client_secret = get_client_secret(tenant_id, "dmc")
    config = settings.dmc  # DmcSettings instance
    return DmcRestClient(config, client_id, client_secret, token_manager, is_dmc=True, soeid=soeid) 