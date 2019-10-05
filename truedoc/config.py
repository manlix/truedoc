"""Config."""

import datetime

from truedoc.constants import TIME


class Config:  # pylint: disable=too-few-public-methods
    """Common setting variables."""

    class DB:
        """Database-related variables."""

        DIALECT = 'mysql'
        DRIVER = 'pymysql'
        USER = 'truedoc'
        PASSWORD = 'truedoc'
        HOST = 'truedoc-mysql'
        DATABASE = 'truedoc'

        # See: https://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine
        PATH = f'{DIALECT}+{DRIVER}://{USER}:{PASSWORD}@{HOST}/{DATABASE}'

    class DocumentProcessing:
        """Document processing-related variables"""

        SAVE_TO_DIR = '/upload'

        @staticmethod
        def save_to(document_id):
            return f'{Config.DocumentProcessing.SAVE_TO_DIR}/{document_id}'

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
