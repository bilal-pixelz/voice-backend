from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas, database
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse
from jose import jwt
import os

router = APIRouter()

# OAuth config (example for Google)
config_data = {
    'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID', 'your-google-client-id'),
    'GOOGLE_CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET', 'your-google-client-secret'),
    'SECRET_KEY': os.getenv('SECRET_KEY', 'supersecret'),
}
config = Config(environ=config_data)
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=config_data['GOOGLE_CLIENT_ID'],
    client_secret=config_data['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get('/login/google')
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth/google/callback')
async def auth_google_callback(request: Request, db: Session = Depends(database.SessionLocal)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    if not user_info:
        raise HTTPException(status_code=400, detail="Google login failed")
    email = user_info['email']
    social_id = user_info['sub']
    user = db.query(models.User).filter_by(email=email).first()
    if not user:
        # User registration logic (associate with company, default role=user)
        raise HTTPException(status_code=400, detail="User not registered. Please contact admin.")
    # Generate JWT token
    jwt_token = jwt.encode({"sub": user.email, "role": user.role.value}, config_data['SECRET_KEY'], algorithm="HS256")
    response = RedirectResponse(url=f"/?token={jwt_token}")
    return response
