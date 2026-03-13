from fastapi import APIRouter
from . import schemas

router = APIRouter()

@router.post("/embeddings/", response_model=schemas.Embedding)
async def create_embedding(text: schemas.TextToEmbed):
    # In a real application, you would use a sentence transformer model here.
    # For now, we'll return a dummy embedding.
    return {"embedding": [0.1, 0.2, 0.3, 0.4]}
