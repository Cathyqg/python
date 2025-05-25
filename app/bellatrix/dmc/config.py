from pydantic import BaseModel
from typing import List

class DmcrSettings(BaseModel):
    active: bool
    hostname: str
    x_dmcr_apic_header: str
    x_dmcr_authentication: str
    doc_type_codes: List[str]
    page_size: int

class DmcSettings(BaseModel):
    active: bool
    hostname: str
    x_dmc_apic_header: str
    x_dmc_authentication: str
    doc_type_codes: List[str]
    page_size: int 