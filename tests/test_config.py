import datetime
import pytest

import truedoc.common
import truedoc.config


class TestConfigCelery:
    """Test config class 'Celery."""

    def test_constants(self):
        assert truedoc.config.Celery.CONFIG == {
            'result_backend': 'amqp',
            'result_persistent': True,
            'broker_transport_options': {

                "max_retries": 3,
                "interval_start": 0,
                "interval_step": 0.4,
                "interval_max": 0.4,
            }
        }


class TestConfigRabbitmq:
    """Test config class 'Rabbitmq'."""

    def test_constants(self):
        PROTO = 'amqp'
        USER = 'guest'
        PASSWORD = 'guest'
        HOST = 'truedoc-rabbitmq'

        assert PROTO == truedoc.config.Rabbitmq.PROTO
        assert USER == truedoc.config.Rabbitmq.USER
        assert PASSWORD == truedoc.config.Rabbitmq.PASSWORD
        assert HOST == truedoc.config.Rabbitmq.HOST

        assert truedoc.config.Rabbitmq.PATH == f'{PROTO}://{USER}:{PASSWORD}@{HOST}'


class TestConfigDatabase:
    """Test config class 'Database'."""

    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USER = 'truedoc'
    PASSWORD = 'truedoc'
    HOST = 'truedoc-mysql'
    DATABASE = 'truedoc'

    def test_constants(self):
        assert self.DIALECT == truedoc.config.Database.DIALECT
        assert self.DRIVER == truedoc.config.Database.DRIVER
        assert self.USER == truedoc.config.Database.USER
        assert self.PASSWORD == truedoc.config.Database.PASSWORD
        assert self.HOST == truedoc.config.Database.HOST
        assert self.DATABASE == truedoc.config.Database.DATABASE

        assert truedoc.config.Database.PATH == f'{self.DIALECT}+{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}/{self.DATABASE}'


class TestConfigDocumentProcessing:
    """Test config class 'DocumentProcessing'."""

    SAVE_TO_DIR = '/upload'

    def test_constants(self):
        assert self.SAVE_TO_DIR == truedoc.config.DocumentProcessing.SAVE_TO_DIR


@pytest.mark.parametrize('document_id', [truedoc.common.uuid4()])
def test_config_documentprocessing_save_to(document_id):
    assert f'{TestConfigDocumentProcessing.SAVE_TO_DIR}/{document_id}' == \
           truedoc.config.DocumentProcessing.save_to(document_id)


class TestConfigToken:
    """Test config class 'Token'."""

    ALGORITHM = 'HS256'
    SECRET = 'secret'

    LEEWAY = 10  # seconds

    ACCESS_TOKEN_EXP = 600  # 10 * 60
    REFRESH_TOKEN_EXP = 900  # 15 * 60

    def test_constants(self):
        assert self.ALGORITHM == truedoc.config.Token.ALGORITHM
        assert self.SECRET == truedoc.config.Token.SECRET
        assert self.LEEWAY == truedoc.config.Token.LEEWAY

        assert self.ACCESS_TOKEN_EXP == truedoc.config.Token.ACCESS_TOKEN_EXP
        assert self.REFRESH_TOKEN_EXP == truedoc.config.Token.REFRESH_TOKEN_EXP


@pytest.mark.parametrize('timedelta', [TestConfigToken.ACCESS_TOKEN_EXP, TestConfigToken.REFRESH_TOKEN_EXP])
def test_config_token_expiration_time(timedelta):
    assert datetime.datetime.utcnow() + datetime.timedelta(seconds=timedelta) > datetime.datetime.utcnow()
