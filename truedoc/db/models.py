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


class BookmytimeDate(Model):
    """Bookmytime: 'Date' model."""
    __tablename__ = 'bookmytime_date'

    # TODO: see about 'relationship'
    date_id = Column(VARCHAR(36), primary_key=True)  # UUID
    profile_id = Column(VARCHAR(36), ForeignKey(Profile.profile_id), nullable=False)  # UUID
    date = Column(DATE, nullable=False)

    UniqueConstraint(profile_id, date)  # One 'date' on each 'profile_id' only.

    def __init__(self, profile_id, date):
        self.__set_profile_id(profile_id)
        self.__set_date(date)
        self.__set_date_id()

    def __repr__(self):
        return f'<Date date_id={self.date_id}>'

    def __set_date_id(self):
        self.date_id = common.uuid4()

    def __set_date(self, date):
        self.date = date

    def __set_profile_id(self, profile_id):
        self.profile_id = profile_id


class BookmytimeTime(Model):
    """Bookmytime: 'Time' model."""
    __tablename__ = 'bookmytime_time'

    # TODO: see about 'relationship'
    time_id = Column(VARCHAR(36), primary_key=True)
    date_id = Column(VARCHAR(36), ForeignKey(BookmytimeDate.date_id), nullable=False)
    time = Column(TIME, nullable=False)
    appointment_id = Column(VARCHAR(36), nullable=True)

    UniqueConstraint(date_id, time)  # Only unique time is allowed in the slot.

    def __init__(self, date_id, time):
        self.__set_date_id(date_id)
        self.__set_time(time)
        self.__set_time_id()

    def __repr__(self):
        return f'<Time time_id={self.time_id}>'

    def __set_time_id(self):
        self.time_id = common.uuid4()

    def __set_time(self, time):
        self.time = time

    def __set_date_id(self, day_id):
        self.date_id = day_id


class BookmytimeAppointment(Model):
    """Bookmytime: 'Appointment' model."""
    __tablename__ = 'bookmytime_appointment'

    # TODO: see about 'relationship'
    appointment_id = Column(VARCHAR(36), default=common.uuid4, primary_key=True)
    time_id = Column(VARCHAR(36), ForeignKey(BookmytimeTime.time_id), nullable=False)
