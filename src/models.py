from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


association_table = db.Table(
    "association",
    db.Model.metadata,
    db.Column("tournament_id", db.ForeignKey("tournament.id")),
    db.Column("fencer", db.ForeignKey("fencer.id")),
)

class Tournament(db.Model):
    __tablename__ = "tournament"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow,)
    
class Fencer(db.Model):
    __tablename__ = "fencer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=True)
    rating = db.Column(db.String(1), default="U")
    tournaments = db.relationship(
        "Tournament", secondary=association_table, backref="fencers"
    )
