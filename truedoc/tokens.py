"""Work with tokens."""

import jwt

import truedoc.config
import truedoc.exceptions


def create_token(profile_id, expiration_time) -> str:
    """Create token for given 'profile_id' with 'expiration_time'."""

    payload = dict(
        exp=truedoc.config.Token.expiration_time(expiration_time),
        profile_id=profile_id,
    )

    token = jwt.encode(
        payload=payload,
        algorithm=truedoc.config.Token.ALGORITHM,
        key=truedoc.config.Token.SECRET,
    )

    return token


def create_tokens(profile_id) -> dict:
    """Create both access and refresh tokens."""
    return {
        'access_token': create_token(profile_id, truedoc.config.Token.ACCESS_TOKEN_EXP),
        'refresh_token': create_token(profile_id, truedoc.config.Token.REFRESH_TOKEN_EXP),
    }


def is_token_valid(token) -> bool:
    """Check access_token."""

    try:
        decoded = jwt.decode(
            jwt=token,
            key=truedoc.config.Token.SECRET,
            leeway=truedoc.config.Token.LEEWAY,
            algorithms=[
                truedoc.config.Token.ALGORITHM,
            ],
            options={
                'require_exp': True,
                'verify_exp': True,
                'verify_signature': True,
            }

        )

    except jwt.exceptions.PyJWTError as exc:
        raise truedoc.exceptions.TokenError(exc)

    if isinstance(decoded, dict):  # ATTENTION: over-secure approach to return 'True' if result is 'dict' only
        return True
