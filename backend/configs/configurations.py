import os
from pathlib import Path
from google_auth_oauthlib.flow import Flow

react_app = "http://localhost:3000"


def google_flow(host):
    return Flow.from_client_secrets_file(
        client_secrets_file=os.path.join(Path(f"{os.path.abspath('./env')}"), "client_secrets.json"),
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
                "openid"],
        redirect_uri=f"{host}/callback"
    )


def get_ref():
    return react_app
