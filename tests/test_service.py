"""
Functional testing at API level.
"""

import json


def test_hello(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """

    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data


def test_check_db_ctx(test_client):
    """
    GIVEN a Flask application AND a init db with mocked data
    WHEN the /checkDbConnection is requested (GET)
    THEN the response should contains the inserted first row
    """

    response = test_client.get("/checkDbConnection")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["job_reference"] == "job1"
    assert data["organization_reference"] == "michel_corp"
    assert data["profession_id"] == 1
    assert data["office_latitude"] == 48.866683
    assert data["office_longitude"] == 2.342687
    assert data["office_continent"] is None
    assert data["candidates"] == 3


def test_consolidate_data(test_client):
    """
    GIVEN a Flask application AND a init db with mocked data
    WHEN the /consolidateData is requested (GET)
    AND /checkDbConnection is requested (GET)
    THEN the response should contains the inserted first row with updated continent
    """

    test_client.get("/consolidateData")
    response = test_client.get("/checkDbConnection")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["office_continent"] == "EUROPE"


def test_get_jobs_by_continent(test_client):
    """
    GIVEN a Flask application AND a init db with mocked data
    WHEN the /consolidateData is requested (GET)
    AND /jobsByContinent is requested (POST) with 1 correct profession_id
    THEN the response should contains the right aggregated jobs by continent
    """

    test_client.get("/consolidateData")

    mimetype = "application/json"
    headers = {"Content-Type": mimetype}
    data = {"profession_ids": [1]}
    url = "/jobsByContinent"

    response = test_client.post(url, json=data, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["ASIA"] == 1
    assert data["EUROPE"] == 4
    assert data["OTHERS"] == 1


def test_get_jobs_by_continent_multiple_profession_ids(test_client):
    """
    GIVEN a Flask application AND a init db with mocked data
    WHEN the /consolidateData is requested (GET)
    AND /jobsByContinent is requested (POST) with 2 correct profession_ids
    THEN the response should contains the right aggregated jobs by continent
    """

    test_client.get("/consolidateData")

    mimetype = "application/json"
    headers = {"Content-Type": mimetype}
    data = {"profession_ids": [1, 4]}
    url = "/jobsByContinent"

    response = test_client.post(url, json=data, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["ASIA"] == 2
    assert data["EUROPE"] == 4
    assert data["OTHERS"] == 1


def test_get_jobs_by_continent_malformed_body(test_client):
    """
    GIVEN a Flask application AND a init db with mocked data
    WHEN the /consolidateData is requested (GET)
    AND /jobsByContinent is requested (POST) with wrong values
    THEN 400 error response should be returned
    """

    test_client.get("/consolidateData")

    mimetype = "application/json"
    headers = {"Content-Type": mimetype}
    url = "/jobsByContinent"

    # Negative value
    data = {"profession_ids": [-1]}
    response = test_client.post(url, json=data, headers=headers)
    assert response.status_code == 400

    # Wrong data type
    data = {"profession_ids": "Not a list"}
    response = test_client.post(url, json=data, headers=headers)
    assert response.status_code == 400

    # Empty list
    data = {"profession_ids": []}
    response = test_client.post(url, json=data, headers=headers)
    assert response.status_code == 400

    # Wrong key
    data = {"wrongkey": [1]}
    response = test_client.post(url, json=data, headers=headers)
    assert response.status_code == 400


def test_get_jobs_by_continent_not_found(test_client):
    """
    GIVEN a Flask application AND a init db with mocked data
    WHEN the /consolidateData is requested (GET)
    AND /jobsByContinent is requested (POST) with unknown profession_ids
    THEN 404 error response should be returned
    """

    test_client.get("/consolidateData")

    mimetype = "application/json"
    headers = {"Content-Type": mimetype}
    url = "/jobsByContinent"

    data = {"profession_ids": [999]}
    response = test_client.post(url, json=data, headers=headers)
    assert response.status_code == 404
