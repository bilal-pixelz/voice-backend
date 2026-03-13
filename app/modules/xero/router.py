from fastapi import APIRouter

router = APIRouter()

@router.get("/invoices")
async def get_xero_invoices():
    return {"module": "xero"}