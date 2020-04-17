"""
Contains interfaces for database comunication layer.
"""

from abc import ABC, abstractmethod
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from whyemetl import models


class JobsRepository(ABC):
    """
    Repository interface to interact with Jobs model.
    """

    @abstractmethod
    def get_first_job(self) -> models.Jobs:
        """ Returns the first row among jobs. """
        pass

    @abstractmethod
    def get_jobs(self) -> List[models.Jobs]:
        """ Returns all the jobs. """
        pass

    @abstractmethod
    def get_jobs_count(self) -> int:
        """ Returns total rows count. """
        pass

    @abstractmethod
    def update_jobs(self) -> None:
        """ Updates staged jobs to database. """
        pass

    @abstractmethod
    def get_jobs_by_continent(self, profession_ids: List[int]) -> List[models.Jobs]:
        """
        Returns the aggregated jobs information by continent given
        the profession_ids.
        """
        pass


class SQLJobsRepository(JobsRepository):
    """
    SQL implementation of JobsRepository using SQLAlchemy.
    """

    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def get_first_job(self) -> models.Jobs:
        return self.db.session.query(models.Jobs).first()

    def get_jobs(self) -> List[models.Jobs]:
        return self.db.session.query(models.Jobs).all()

    def get_jobs_count(self) -> int:
        return self.db.session.query(models.Jobs).count()

    def update_jobs(self) -> None:
        self.db.session.commit()

    def get_jobs_by_continent(self, profession_ids: List[int]) -> List[models.Jobs]:
        return (
            self.db.session.query(
                models.Jobs.office_continent,
                func.sum(models.Jobs.candidates).label("total_candidates"),
            )
            .filter(models.Jobs.profession_id.in_(profession_ids))
            .group_by(models.Jobs.office_continent)
            .all()
        )
