import datetime

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.types import DATE
from sqlalchemy.types import DATETIME
from sqlalchemy.types import INTEGER
from sqlalchemy.types import TIME
from sqlalchemy.types import VARCHAR

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import truedoc.config
import truedoc.exceptions

from truedoc import common

# Standard naming convention:
# https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

engine = create_engine(truedoc.config.Database.PATH, echo=True)
metadata = MetaData(bind=engine, naming_convention=convention)
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


class Day(Model):
    """Days model."""
    __tablename__ = 'day'

    # TODO: see about 'relationship'
    day_id = Column(VARCHAR(36), primary_key=True)  # UUID
    profile_id = Column(VARCHAR(36), ForeignKey('profile.profile_id'), nullable=False)  # UUID
    date = Column(DATE, nullable=False)

    UniqueConstraint(profile_id, date)  # One 'date' on each 'profile_id' only.

    def __init__(self, profile_id, date):
        self.__set_day_id()
        self.__set_profile_id(profile_id)
        self.__set_date(date)

    def __repr__(self):
        return f'<Day day_id={self.day_id}>'

    def __set_day_id(self):
        self.day_id = common.uuid4()

    def __set_date(self, date):
        self.date = date

    def __set_profile_id(self, profile_id):
        self.profile_id = profile_id


class Slot(Model):
    """Slots model."""
    __tablename__ = 'slot'

    # TODO: see about 'relationship'
    slot_id = Column(VARCHAR(36), default=common.uuid4, primary_key=True)
    day_id = Column(VARCHAR(36), ForeignKey('day.day_id'), nullable=False)
    time = Column(TIME, nullable=False)
    appointment_id = Column(VARCHAR(36), nullable=True)


class Appointment(Model):
    """Appointments model."""
    __tablename__ = 'appointment'

    # TODO: see about 'relationship'
    appointment_id = Column(VARCHAR(36), default=common.uuid4, primary_key=True)
    slot_id = Column(VARCHAR(36), ForeignKey('slot.slot_id'), nullable=False)
