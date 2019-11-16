"""Work with JWT: https://tools.ietf.org/html/rfc7519"""

import jwt

import truedoc.config
import truedoc.exceptions
import truedoc.website.context


def create_token(profile_id: str, expiration_time) -> str:
    """Create token for given 'profile_id' with 'expiration_time'.

    :param profile_id: profile_id
    :param expiration_time: expiration token time
    :return: token with fixed expiration time
    """

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


def create_tokens(profile_id: str) -> dict:
    """Create both access and refresh tokens.

    :param profile_id: profile id
    :return: dict with both access and refresh tokens
    """
    return {
        'access_token': create_token(profile_id, truedoc.config.Token.ACCESS_TOKEN_EXP),
        'refresh_token': create_token(profile_id, truedoc.config.Token.REFRESH_TOKEN_EXP),
    }


def is_valid_token(token: str, save_to_ctx: bool = True) -> bool:
    """Check token and return dict if its is valid.

    :param token: token to validate
    :param save_to_ctx: default is 'True' — save token to request context.
    :return: boolean
    """
    try:
        decoded_token = jwt.decode(
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

    if save_to_ctx:
        truedoc.website.context.add("token", decoded_token)

    return isinstance(decoded_token, dict)
