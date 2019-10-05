import datetime

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.types import DATETIME
from sqlalchemy.types import INTEGER
from sqlalchemy.types import VARCHAR

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import truedoc.config
import truedoc.exceptions

from truedoc import common

engine = create_engine(truedoc.config.Database.PATH, echo=True)
metadata = MetaData(bind=engine)
Model = declarative_base(metadata=metadata)


class Profile(Model):
    """Profile model."""
    __tablename__ = 'profile'

    profile_id = Column(VARCHAR(36), default=common.uuid4, primary_key=True)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(128), nullable=False)
    created_at = Column(DATETIME, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, email):
        self.__set_email(email)

    def __repr__(self):
        return f'<User profile_id={self.profile_id}>'

    def __set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if check_password_hash(self.password, password):
            return True

        raise truedoc.exceptions.ProfileInvalidPassword


class Document(Model):
    """Document model."""
    __tablename__ = 'document'

    document_id = Column(VARCHAR(36), primary_key=True)  # Unique document ID
    profile_id = Column(VARCHAR(36), ForeignKey('profile.profile_id'), nullable=False)
    title = Column(VARCHAR(128), nullable=True)  # Document title

    filename = Column(VARCHAR(256), nullable=False)  # Document filename like 'data.txt'
    filesize = Column(INTEGER, nullable=False)  # Document size in bytes
    digest = Column(VARCHAR(32), nullable=False)  # MD5 of the document
    created_at = Column(DATETIME, nullable=False)  # UTC
