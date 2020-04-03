import pytest

from whyemetl import create_app, db
from whyemetl.location import Position, Rectangle
from whyemetl.models import Jobs

#
# Fixture for location module testing
#


@pytest.fixture(scope="session")
def rectangular_europe():
    """ Raw approximation of Europe Area """
    upperleft = Position(58.950306, -17.455528)  # North-West of UK
    bottomright = Position(42.324367, 27.273977)  # South-East of Bulgaria
    return Rectangle("europe", upperleft, bottomright)


@pytest.fixture(scope="session")
def rectangular_america():
    """ Raw approximation of America Area """
    upperleft = Position(71.608584, -168.455893)  # Somewhere in Chukchi Sea
    bottomright = Position(23.437493, -52.142073)  # North-east or Porto Rico
    return Rectangle("america", upperleft, bottomright)


@pytest.fixture(scope="session")
def rectangular_asia():
    """ Raw approximation of America Area """
    upperleft = Position(71.654537, 37.787070)  # Somewhere in Barents Sea
    bottomright = Position(15.050491, 144.707127)  # Somewhere in the Philippine Sea
    return Rectangle("asia", upperleft, bottomright)


#
# Fixture for models module testing
#


@pytest.fixture(scope="function")
def new_job():
    return Jobs(
        job_reference="job1234",
        organization_reference="michel_organization",
        profession_id=1,
        office_latitude=48.866683,
        office_longitude=2.342687,
        office_continent="europe",
        candidates=3,
    )


#
# Fixture for functional/service testing
#


@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.testing = True
    testing_client = app.test_client()

    with app.app_context():

        # Create the database and the database table
        db.create_all()

        # Organization 1
        # Europe
        # 2 different jobs with 2 different professions
        job1 = Jobs(
            job_reference="job1",
            organization_reference="michel_corp",
            profession_id=1,
            office_latitude=48.866683,
            office_longitude=2.342687,
            # continent not initialized (should be Europe)
            candidates=3,
        )

        job2 = Jobs(
            job_reference="job2",
            organization_reference="michel_corp",
            profession_id=2,
            office_latitude=48.866683,
            office_longitude=2.342687,
            # continent not initialized (should be Europe)
            candidates=1,
        )

        # Organization 2
        # Europe
        # 1 job with same profession of job1
        job3 = Jobs(
            job_reference="job3",
            organization_reference="toto_corp",
            profession_id=1,
            office_latitude=48.866683,
            office_longitude=2.342687,
            # continent not initialized (should be Europe)
            candidates=1,
        )

        # Organization 3
        # Asia
        # 2 jobs with 2 different professions. 1 is same than in Europe
        job4 = Jobs(
            job_reference="job4",
            organization_reference="beijing_corp",
            profession_id=1,
            office_latitude=39.880066,
            office_longitude=116.388496,
            # continent not initialized (should be Asia)
            candidates=1,
        )

        job5 = Jobs(
            job_reference="job5",
            organization_reference="beijing_corp",
            profession_id=4,
            office_latitude=39.880066,
            office_longitude=116.388496,
            # continent not initialized (should be Asia)
            candidates=1,
        )

        # Organization 4
        # Far south of Earth
        # 1 random job
        job6 = Jobs(
            job_reference="job6",
            organization_reference="nowhere_corp",
            profession_id=1,
            office_latitude=-66.123957,
            office_longitude=29.799831,
            # continent not initialized (should be OTHERS)
            candidates=1,
        )

        # Add mocked data in mocked db
        db.session.add(job1)
        db.session.add(job2)
        db.session.add(job3)
        db.session.add(job4)
        db.session.add(job5)
        db.session.add(job6)
        db.session.commit()

        yield testing_client

        db.drop_all()
