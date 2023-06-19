import os

import jwt
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

token_auth_scheme = HTTPBearer(auto_error=False)


class VerifyToken:
    def __init__(self, token: HTTPAuthorizationCredentials) -> None:
        self.token = token.credentials
        self.config = {
            "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
            "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
            "ISSUER": os.getenv("ISSUER", "https://your.domain.com/"),
            "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
        }
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        self.signing_key = self.jwks_client.get_signing_key_from_jwt(self.token).key
        payload = jwt.decode(
            self.token,
            self.signing_key,
            algorithms=self.config["ALGORITHMS"],
            audience=self.config["API_AUDIENCE"],
            issuer=self.config["ISSUER"],
        )
        return payload


def verify_token(
    res: Response,
    credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required.",
            headers={"WWW-Authenticate": 'Bearer realm="auth_required"'},
        )

    try:
        payload = VerifyToken(credentials).verify()
    except BaseException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {e}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    res.headers["WWW-Authenticate"] = 'Bearer realm="auth_required"'
    return payload
