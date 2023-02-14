from app.common.models import SimpleMessageResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=SimpleMessageResponse)
async def home():
    return {"message": "Visit /docs for OpenAPI Specs"}

# For k8s healthiness probe
@router.get("/healthz", response_model=SimpleMessageResponse)
async def health():
    return {"message": "OK"}
