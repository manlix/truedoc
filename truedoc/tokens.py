"""Work with tokens."""

import jwt
from truedoc.config import Config
import truedoc.exceptions


def create_token(profile_id, expiration_time) -> str:
    """Create token for given 'profile_id' with 'expiration_time'."""

    payload = dict(
        exp=Config.Token.expiration_time(expiration_time),
        profile_id=profile_id,
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


def check_token(token):
    """Check access_token."""

    try:
        decoded = jwt.decode(
            jwt=token,
            key=Config.Token.SECRET,
            leeway=Config.Token.LEEWAY,
            algorithms=[
                Config.Token.ALGORITHM,
            ],
            options={
                'require_exp': True,
                'verify_exp': True,
                'verify_signature': True,
            }

        )

    except jwt.exceptions.PyJWTError as exc:
        raise truedoc.exceptions.JWTError(exc)

    if isinstance(decoded, dict):
        return True
