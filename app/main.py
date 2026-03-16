import os
from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from app.core.response import create_response
from app.modules.auth.router import router as auth_router
from app.core.config import settings
from app.modules.embeddings.router import router as embeddings_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Voice2Invoice API")

if settings.ENVIRONMENT == "development":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
else:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'


origins = []
if settings.CORS_ORIGINS:
    origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)

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