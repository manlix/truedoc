"""Useful docs:
    1) All error codes for PyMySQL: https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/constants/ER.py
    2) Difficult queries for SQLAlchemy: https://habrahabr.ru/company/eastbanctech/blog/226521/

To catch original exception from PyMySQL dig to "exc.orig":
    - exc.orig.args[0] - error code
    - exc.orig.args[1] - error message
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from sqlalchemy.exc import IntegrityError
from pymysql.constants import ER

from . import models
from truedoc.exceptions import ProfileAlreadyExistsError, ProfileDoesNotExist

db_session = scoped_session(sessionmaker(bind=models.engine))


class Profile:

    @staticmethod
    def list_all():
        """List all profiles."""
        query = db_session.query(models.Profile).all()

        return query

    @staticmethod
    def create(profile: models.Profile) -> None:
        """Create profile."""
        db_session.add(profile)

        try:
            db_session.commit()
        except IntegrityError as exc:
            db_session.rollback()

            errno, errmsg = exc.orig.args

            if errno == ER.DUP_ENTRY:
                raise ProfileAlreadyExistsError

            raise


class Document:

    @staticmethod
    def list_all():
        """List all documents."""
        query = db_session.query(models.Document).all()

        return query

    @staticmethod
    def create(document: models.Document):
        """Create document."""
        db_session.add(document)

        try:
            db_session.commit()
        except IntegrityError as exc:
            db_session.rollback()

            errno, errmsg = exc.orig.args

            if errno == ER.NO_REFERENCED_ROW_2:
                raise ProfileDoesNotExist

            raise
