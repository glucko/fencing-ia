from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


association_table = db.Table(
    "association",
    db.Model.metadata,
    db.Column("tournament_id", db.ForeignKey("tournament.id")),
    db.Column("competitor_id", db.ForeignKey("competitor.id")),
)

class Tournament(db.Model):
    __tablename__ = "tournament"
    id = db.Column(db.Integer, primary_key=True)
    
class Competitor(db.Model):
    __tablename__ = "competitor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    tournaments = db.relationship(
        "Tournament", secondary=association_table, backref="competitors"
    )
