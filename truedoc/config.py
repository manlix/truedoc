"""Project configuration."""

import datetime

from truedoc.constants import TIME


class Celery:
    """Celery-related variables."""

    CONFIG = {
        'result_backend': 'amqp',
        'result_persistent': True,
        'broker_transport_options': {

            # See about 'Retry Policy": https://docs.celeryproject.org/en/master/userguide/calling.html#retry-policy
            "max_retries": 3,
            "interval_start": 0,
            "interval_step": 0.4,
            "interval_max": 0.4,
        }
    }


class Rabbitmq:
    """RabbitMQ broker-related variables."""

    PROTO = 'amqp'
    USER = 'guest'
    PASSWORD = 'guest'
    HOST = 'truedoc-rabbitmq'

    PATH = f'{PROTO}://{USER}:{PASSWORD}@{HOST}'


class Database:
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
        return f'{DocumentProcessing.SAVE_TO_DIR}/{document_id}'


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
