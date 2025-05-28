# Shared secret fetching utilities for DMC/DMCR

def get_client_id(tenant_id: str, system: str) -> str:
    # system: "dmc" or "dmcr"
    # TODO: Fetch from Vault or secret manager
    # Example:
    # secret = vault_client.get_secret(f"{system}/{tenant_id}")
    # return secret["client_id"]
    return "example_client_id"

def get_client_secret(tenant_id: str, system: str) -> str:
    # TODO: Fetch from Vault or secret manager
    # Example:
    # secret = vault_client.get_secret(f"{system}/{tenant_id}")
    # return secret["client_secret"]
    return "example_client_secret" 