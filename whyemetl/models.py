"""
Contains ORM database tables models for database communication.
"""

from whyemetl import db


class Jobs(db.Model):
    job_reference = db.Column(db.String, primary_key=True)
    organization_reference = db.Column(db.String)
    profession_id = db.Column(db.Integer)
    office_latitude = db.Column(db.Float)
    office_longitude = db.Column(db.Float)
    office_continent = db.Column(db.String)
    candidates = db.Column(db.Integer)

    def __repr__(self):
        return "<Job Reference %r>" % self.job_reference
