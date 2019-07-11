"""Useful docs:
    1) All error codes for PyMySQL: https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/constants/ER.py
    2) Difficult queries for SQLAlchemy: https://habrahabr.ru/company/eastbanctech/blog/226521/

To catch original exception from PyMySQL dig to "exc.orig":
    - exc.orig.args[0] - error code
    - exc.orig.args[1] - error message
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from . import models

db_session = scoped_session(sessionmaker(bind=models.engine))


class Profile:

    @staticmethod
    def list_all():
        """List all profiles."""
        query = db_session.query(models.Profile).all()

        return query

    @staticmethod
    def create_profile(profile: models.Profile) -> None:
        """Create profile."""
        db_session.add(profile)
        db_session.commit()

