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

        LEEWAY = 10 * TIME.SECOND

        ACCESS_TOKEN_EXP = 10 * TIME.MINUTE
        REFRESH_TOKEN_EXP = 15 * TIME.MINUTE

        @staticmethod
        def expiration_time(timedelta):
            return datetime.datetime.utcnow() + datetime.timedelta(seconds=timedelta)
