"""Config."""

import datetime

from truedoc.constants import TIME


class Config:  # pylint: disable=too-few-public-methods
    """Common setting variables."""
    DB_PATH = 'mysql+pymysql://truedoc:truedoc@truedoc-mysql/truedoc'

    class Token:
        """Data for work with JWT."""
        ALGORITHM = 'HS256'
        SECRET = 'secret'  # TODO: think where we can to save it securely
        ISSUER = 'truedoc-app'

        ACCESS_TOKEN_EXP = TIME.MINUTE * 10
        REFRESH_TOKEN_EXP = TIME.MINUTE * 15

        @staticmethod
        def expiration_time(timedelta):
            return datetime.datetime.utcnow() + datetime.timedelta(seconds=timedelta)
