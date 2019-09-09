"""Work with tokens."""

import datetime

import jwt
from truedoc.config import Config


def create_token(profile_id, expiration_time) -> str:
    """Create token for given 'profile_id' with 'expiration_time'."""

    payload = dict(
        iss=Config.Token.ISSUER,
        exp=Config.Token.expiration_time(expiration_time),
        iat=datetime.datetime.utcnow(),

        profile_id=profile_id,  # Required field.
    )

    token = jwt.encode(
        payload=payload,
        algorithm=Config.Token.ALGORITHM,
        key=Config.Token.SECRET,
    )

    return token


def create_tokens(profile_id) -> dict:
    """Create both access and refresh tokens."""
    return {
        'access_token': create_token(profile_id, Config.Token.ACCESS_TOKEN_EXP),
        'refresh_token': create_token(profile_id, Config.Token.REFRESH_TOKEN_EXP),
    }
