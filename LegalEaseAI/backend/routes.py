from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.get("/health")
def health():
    return {
        "status": "ok",
        "gemini_configured": True,
        "model": generator.model_name
    }


@router.post("/generate")
def generate_document(request: DocumentRequest):

    try:
        generated_text = generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates
        )

        return {
            "document_type": request.document_type,
            "generated_text": generated_text
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )