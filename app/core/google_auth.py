from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from app.core.config import settings

# This is the scope that we will request from the user
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]

# This is the client config that we will use to generate the flow
CLIENT_CONFIG = {
    "web": {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "project_id": "voice-backend", # This can be anything
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uris": settings.GOOGLE_FRONTEND_REDIRECT_URI
    }
}


def get_google_auth_flow(state=None):
    """
    Returns a Google OAuth2 flow object.
    """
    print('redirect_uri', CLIENT_CONFIG["web"]["redirect_uris"][0])
    flow = Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=SCOPES,
        state=state,
        redirect_uri=CLIENT_CONFIG["web"]["redirect_uris"][0],
    )

    return flow


def get_user_info_from_google(credentials):
    """
    Returns user info from Google.
    """
    token_request = Request()
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=settings.GOOGLE_CLIENT_ID
    )

    return id_info
