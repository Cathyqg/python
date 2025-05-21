from pydantic import BaseSettings, Field
from typing import Dict, Optional

class Settings(BaseSettings):
    # S3
    s3_bucket: str = Field(..., env="S3_BUCKET")
    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field("us-east-1", env="AWS_REGION")

    # DMCR
    dmcr_base_url: str = Field(..., env="DMCR_BASE_URL")
    dmcr_fid: str = Field(..., env="DMCR_FID")
    dmcr_password: str = Field(..., env="DMCR_PASSWORD")
    # Optionally, a mapping of documentId to file path/URL
    dmcr_document_map: Optional[Dict[str, str]] = None

    # DMC (future)
    dmc_base_url: Optional[str] = None
    dmc_fid: Optional[str] = None
    dmc_password: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings() 