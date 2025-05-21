# Python File Service

This service exposes two endpoints:
- `POST /files/upload`: Download a file from DMCR, upload to S3, generate an embedding, and store metadata.
- `GET /files/{file_id}/metadata`: Retrieve stored metadata.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables for S3 and DMCR credentials (see `.env.example`).
3. Run the service:
   ```bash
   uvicorn app.main:app --reload
   ```

## Extending
- To add DMC support, implement `services/dmc.py` and update the service layer.
- To use a real embedding model, update `services/embedding.py`. 