"""
Contains interfaces for database comunication layer.
"""

from abc import ABC, abstractmethod

from sqlalchemy import func

from whyemetl.models import Jobs


class JobsRepository(ABC):
    """
    Repository interface to interact with Jobs model.
    """

    @abstractmethod
    def get_first_job(self):
        """ Returns the first row among jobs. """
        pass

    @abstractmethod
    def get_jobs(self):
        """ Returns all the jobs. """
        pass

    @abstractmethod
    def get_jobs_count(self):
        """ Returns total rows count. """
        pass

    @abstractmethod
    def update_jobs(self):
        """ Updates staged jobs to database. """
        pass

    @abstractmethod
    def get_jobs_by_continent(self, profession_ids):
        """
        Returns the aggregated jobs information by continent given
        the profession_ids.
        """
        pass


class SQLJobsRepository(JobsRepository):
    """
    SQL implementation of JobsRepository using SQLAlchemy.
    """

    def __init__(self, db):
        self.db = db

    def get_first_job(self):
        return self.db.session.query(Jobs).first()

    def get_jobs(self):
        return self.db.session.query(Jobs).all()

    def get_jobs_count(self):
        return self.db.session.query(Jobs).count()

    def update_jobs(self):
        self.db.session.commit()

    def get_jobs_by_continent(self, profession_ids):
        return (
            self.db.session.query(
                Jobs.office_continent,
                func.sum(Jobs.candidates).label("total_candidates"),
            )
            .filter(Jobs.profession_id.in_(profession_ids))
            .group_by(Jobs.office_continent)
            .all()
        )
