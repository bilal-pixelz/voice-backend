from datetime import timedelta
import secrets
import hashlib
import base64
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.google_auth import get_google_auth_flow, get_user_info_from_google
from app.core.response import create_response
from app.core.security import (
    create_access_token,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.modules.auth.repository import UserRepo
from app.modules.auth import schemas

router = APIRouter()


@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = UserRepo.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = UserRepo.create_user(db=db, user=user)
    return create_response(
        success=True,
        data=UserRepo.to_dict(created_user),
        message="User created successfully",
    )


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = UserRepo.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return create_response(
        success=True,
        data={"access_token": access_token, "token_type": "bearer"},
        message="Login successful",
    )


@router.get("/google/login")
async def google_login(request: Request):
    """
    Generate a Google login URL with PKCE and return it to the frontend.
    """
    code_verifier = secrets.token_urlsafe(64)
    request.session["code_verifier"] = code_verifier

    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .replace("=", "")
    )

    flow = get_google_auth_flow()
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return create_response(
        success=True,
        data={"authorization_url": authorization_url},
        message="Google login URL generated successfully",
    )


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle the callback from Google after the user has authenticated.
    """
    code_verifier = request.session.get("code_verifier")
    if not code_verifier:
        raise HTTPException(status_code=400, detail="Missing code_verifier from session")
    flow = get_google_auth_flow()
    flow.fetch_token(
        authorization_response=str(request.url), code_verifier=code_verifier
    )

    credentials = flow.credentials
    user_info = get_user_info_from_google(credentials)

    user = UserRepo.get_user_by_email(db, email=user_info["email"])
    if not user:
        user = UserRepo.create_user_for_social_login(db, user_info)

    social_account = UserRepo.get_social_account(
        db, provider="google", provider_user_id=user_info["sub"]
    )
    if not social_account:
        UserRepo.create_social_account(
            db, user_id=user.id, provider="google", provider_user_id=user_info["sub"]
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return create_response(
        success=True,
        data={"access_token": access_token, "token_type": "bearer"},
        message="Login successful",
    )
