"""Useful docs:
    1) All error codes for PyMySQL: https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/constants/ER.py
    2) Difficult queries for SQLAlchemy: https://habrahabr.ru/company/eastbanctech/blog/226521/

To catch original exception from PyMySQL dig to "exc.orig":
    - exc.orig.args[0] - error code
    - exc.orig.args[1] - error message
"""

from typing import (
    List,
    NoReturn,
)

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import IntegrityError
from pymysql.constants import ER

from . import models
from truedoc.exceptions import BookmytimeDateAlreadyExistsError
from truedoc.exceptions import BookmytimeDateDoesNotExist
from truedoc.exceptions import DocumentDoesNotExist
from truedoc.exceptions import ProfileAlreadyExistsError
from truedoc.exceptions import ProfileDoesNotExist
from truedoc.exceptions import ProfileIsNotAvailableForDeleting
from truedoc.exceptions import BookmytimeTimeAlreadyExistsError
from truedoc.exceptions import BookmytimeViolationError

db_session = scoped_session(sessionmaker(bind=models.engine))


class Profile:

    @staticmethod
    def list_all():
        """List all profiles."""
        query = db_session.query(models.Profile).all()

        return query

    @staticmethod
    def create(profile: models.Profile) -> NoReturn:
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

    @staticmethod
    def delete(profile: models.Profile) -> NoReturn:
        """Delete profile."""

        db_session.delete(profile)

        try:
            db_session.commit()
        except IntegrityError as exc:
            db_session.rollback()

            errno, errmsg = exc.orig.args

            if errno == ER.ROW_IS_REFERENCED_2:
                raise ProfileIsNotAvailableForDeleting

            raise

    @staticmethod
    def load(profile_id_or_email: str) -> models.Profile:
        """Load profile by either 'profile_id' or 'email' field."""

        # Load by 'email'
        if '@' in profile_id_or_email:
            query = db_session.query(models.Profile).filter(models.Profile.email == profile_id_or_email).first()

        # Load by 'profile_id'
        else:
            query = db_session.query(models.Profile).filter(models.Profile.profile_id == profile_id_or_email).first()

        if query is None:
            raise ProfileDoesNotExist

        return query


class Document:

    @staticmethod
    def documents(profile_id: str) -> List[models.Document]:
        """List documents by profile_id."

        :param profile_id: profile_id
        :return: list of profile documents
        """

        query = db_session.query(models.Document).filter(models.Document.profile_id == profile_id)

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

    @staticmethod
    def document(document_id: str, profile_id: str) -> models.Document:  # TODO: think how to replace 'str' -> 'uuid'
        """Load document by 'document_id' and 'profile_id'."""

        query = db_session.query(models.Document).filter(
            models.Document.document_id == document_id,
            models.Document.profile_id == profile_id,
        ).first()

        if query is None:
            raise DocumentDoesNotExist

        return query

    @staticmethod
    def delete(document: models.Document) -> None:
        """Delete document."""

        db_session.delete(document)
        db_session.commit()


class BookmytimeDay:

    @staticmethod
    def create(day: models.BookmytimeDate) -> None:
        """Create day."""

        db_session.add(day)

        try:
            db_session.commit()
        except IntegrityError as exc:
            db_session.rollback()

            errno, errmsg = exc.orig.args

            if errno == ER.DUP_ENTRY:
                raise BookmytimeDateAlreadyExistsError

            raise

    @staticmethod
    def by_id(day_id: str) -> bool:
        """Check that given day exists."""
        query = db_session.query(models.BookmytimeDate).filter(
            models.BookmytimeDate.date_id == day_id,
        ).first()

        if query is None:
            raise BookmytimeDateDoesNotExist

        return query


class BookmytimeSlot:

    @staticmethod
    def create(slot: models.BookmytimeTime, profile_id: str) -> NoReturn:
        """Create slot in the day."""

        day = BookmytimeDay.by_id(slot.date_id)

        if day is None or day.profile_id != profile_id:
            raise BookmytimeViolationError

        db_session.add(slot)

        try:
            db_session.commit()
        except IntegrityError as exc:
            db_session.rollback()

            errno, errmsg = exc.orig.args

            if errno == ER.DUP_ENTRY:
                raise BookmytimeTimeAlreadyExistsError

            raise
