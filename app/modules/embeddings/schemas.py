from pydantic import BaseModel
from typing import List

class TextToEmbed(BaseModel):
    text: str

class Embedding(BaseModel):
    embedding: List[float]
