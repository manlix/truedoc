import datetime

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import MetaData

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.types import DATETIME
from sqlalchemy.types import VARCHAR

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .. import common
from ..config import Config

engine = create_engine(Config.DB_PATH, echo=True)
metadata = MetaData(bind=engine)
Model = declarative_base(metadata=metadata)


class Profile(Model):
    """Profile model."""
    __tablename__ = 'profile'

    id = Column(VARCHAR(36), default=common.uuid4, primary_key=True)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(128), nullable=False)
    created_at = Column(DATETIME, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, email):
        self.__set_email(email)

    def __repr__(self):
        return f'<User id={self.id}>'

    def __set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


###########################################################################
#
# WARNING: creating tables in database after all models have been declared.
#
#                       NO DOT REMOVE BELOW.
#
###########################################################################

# TODO: drop when alembic will be implemented
metadata.create_all(engine)
