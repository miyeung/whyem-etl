"""
Contains business logic interfaces.
"""

from abc import ABC, abstractmethod
from typing import List

from whyemetl import america, asia, europe, log, repository
from whyemetl.location import Position, get_continent


class WhyemetlService(ABC):
    """ Main business logic interfaces matching web APIs. """

    def __init__(self, repository: repository.JobsRepository) -> None:
        self.repository = repository

    @abstractmethod
    def check_db_ctx(self) -> dict:
        """ Check connectivity with database. """
        pass

    @abstractmethod
    def consolidate_data(self) -> dict:
        """ Consolidates Jobs data by adding Continent information. """
        pass

    @abstractmethod
    def get_jobs_by_continent(self, profession_ids: List[int]) -> dict:
        """
        Returns the aggregated jobs information by continent given
        the profession_ids.
        """
        pass


class WhyemetlDemoService(WhyemetlService):
    """ Demo implementation of WhyemetlService interface. """

    def __init__(self, repository: repository.SQLJobsRepository) -> None:
        super().__init__(repository)

    def check_db_ctx(self) -> dict:
        job = self.repository.get_first_job()

        return {
            "job_reference": job.job_reference,
            "organization_reference": job.organization_reference,
            "profession_id": job.profession_id,
            "office_latitude": job.office_latitude,
            "office_longitude": job.office_longitude,
            "office_continent": job.office_continent,
            "candidates": job.candidates,
        }

    def consolidate_data(self) -> dict:
        count = self.repository.get_jobs_count()
        jobs = self.repository.get_jobs()

        log.info(f"{count} rows to process")
        log.info("Consolidating data with Continent information...")

        outlier_references = []
        outlier_count = 0

        # Update row by row while computing statistic on number of continents not found
        for job in jobs:
            position = Position(job.office_latitude, job.office_longitude)
            continent = get_continent(position, [europe, asia, america])

            if continent == "OTHERS":
                outlier_references.append(job.job_reference)
                outlier_count += 1
            job.office_continent = continent

        success_rate = 100 - (outlier_count / count * 100)
        log.info("Committing consolidated data to db...")
        self.repository.update_jobs()

        log.info("Consolidated data added to db with success")
        log.info(f"Could not locate Continent for {outlier_count} among {count} rows")
        log.info(f"Consolidation success rate is {success_rate}")

        return {
            "total_processed_rows": count,
            "total_failed_consolidation": outlier_count,
            "consolidation_success_rate": success_rate,
            "failed_rows": outlier_references,
        }

    def get_jobs_by_continent(self, profession_ids: List[int]) -> dict:
        results = self.repository.get_jobs_by_continent(profession_ids)
        if not results:
            raise Exception
        return {row.office_continent.upper(): row.total_candidates for row in results}
