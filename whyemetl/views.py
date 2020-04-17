"""
Contains web API routes logic.
"""

from typing import List

from flask import Blueprint, abort, request

from whyemetl import db, log
from whyemetl.repository import SQLJobsRepository
from whyemetl.service import WhyemetlDemoService

bp = Blueprint("/", __name__)


@bp.route("/")
def hello() -> str:
    return f"Hello, World!"


@bp.route("/checkDbConnection")
def check_db_ctx() -> dict:
    service = WhyemetlDemoService(SQLJobsRepository(db))
    return service.check_db_ctx()


@bp.route("/consolidateData")
def consolidate_data() -> dict:
    service = WhyemetlDemoService(SQLJobsRepository(db))
    return service.consolidate_data()


@bp.route("/jobsByContinent", methods=["POST"])
def get_jobs_by_continent() -> dict:
    profession_ids = request.json.get("profession_ids")
    if malformed_body(profession_ids):
        log.info(f"Request body is malformed: {profession_ids}, returning 400 error")
        abort(400)
    try:
        service = WhyemetlDemoService(SQLJobsRepository(db))
        return service.get_jobs_by_continent(profession_ids)
    except Exception:
        log.info(f"No jobs found for {profession_ids}, returning 404 error")
        abort(404)


def malformed_body(body: List[int]) -> bool:
    if body is None:
        return True
    if not body:
        return True
    if not isinstance(body, list):
        return True
    if any(p < 0 for p in body):
        return True
    return False
