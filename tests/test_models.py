#
# Sanity test for Job model
#


def test_new_job(new_job):
    """
    GIVEN a new Job
    WHEN a Job is created
    THEN check the values
    """

    assert new_job.job_reference == "job1234"
    assert new_job.organization_reference == "michel_organization"
    assert new_job.profession_id == 1
    assert new_job.office_latitude == 48.866683
    assert new_job.office_longitude == 2.342687
    assert new_job.office_continent == "europe"
    assert new_job.candidates == 3
