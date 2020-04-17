"""
Contains ORM database tables models for database communication.
"""

# Workaround to handle no stubs in flask_sqlalchemy resulting in error when
# running mypy
from flask_sqlalchemy.model import DefaultMeta

from whyemetl import db

BaseModel: DefaultMeta = db.Model


class Jobs(BaseModel):
    job_reference = db.Column(db.String, primary_key=True)
    organization_reference = db.Column(db.String)
    profession_id = db.Column(db.Integer)
    office_latitude = db.Column(db.Float)
    office_longitude = db.Column(db.Float)
    office_continent = db.Column(db.String)
    candidates = db.Column(db.Integer)

    def __repr__(self) -> str:
        return "<Job Reference %r>" % self.job_reference
