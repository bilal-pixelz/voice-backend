from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from app.core.response import create_response
from app.modules.auth.router import router as auth_router
from app.modules.embeddings.router import router as embeddings_router

app = FastAPI(title="Voice2Invoice API")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return create_response(
        success=False,
        message=exc.detail,
        status_code=exc.status_code,
        error=[{"type": "http_exception", "detail": exc.detail}]
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return create_response(
        success=False,
        message="Validation Error",
        status_code=422,
        error=exc.errors()
    )

# Create a router for the v1 API
v1_router = APIRouter()

# Include module routers in the v1 router
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(embeddings_router, prefix="/embeddings", tags=["embeddings"])

# Include the v1 router in the main app with the /api prefix
app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to the Voice2Invoice API v1"}