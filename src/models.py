from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

association_table = db.Table(
    "association",
    db.Model.metadata,
    db.Column("tournament_id", db.ForeignKey("tournament.id")),
    db.Column("fencer", db.ForeignKey("fencer.id")),
)

class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id"))
    main_fencer_id = db.Column(db.Integer, db.ForeignKey("fencer.id"))
    opponent_id = db.Column(db.Integer, db.ForeignKey("fencer.id"))
    score = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"Score('{self.main_fencer_id}', '{self.opponent_id}', '{self.score}')"
    
class Tournament(db.Model):
    __tablename__ = "tournament"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime, default=datetime.utcnow,)
    location = db.Column(db.String(80), nullable=True)
    scores = db.relationship("Score", backref="tournament", lazy='dynamic')

    def __repr__(self):
        return f"Tournament('{self.name}', '{self.id}')"
    
class Fencer(db.Model):
    __tablename__ = "fencer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), nullable=True)
    rating = db.Column(db.String(1), default="U")
    tournaments = db.relationship(
        "Tournament", secondary=association_table, backref="fencers"
    )
    def __repr__(self):
        return f"Fencer('{self.name}', '{self.id}', '{self.rating}')"
