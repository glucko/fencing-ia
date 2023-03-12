import click
from flask.cli import with_appcontext
from models import Tournament, Fencer, db


@click.command(name="createdb")
@with_appcontext
def create_db():
    db.create_all()
    db.session.commit()
    print("Database tables created")

@click.command(name="printdb")
@with_appcontext
def print_db():
    tournament = Tournament.query.all()
    fencers = Fencer.query.all()

    for tourn in tournament:
        print("Tournament", tourn.id, tourn.name)
        for user in tourn.fencers:
            print("\t", user.id, user.name)

        for score in tourn.scores.all():
            print("\t", Fencer.query.get(score.main_fencer_id), Fencer.query.get(score.opponent_id), score.score)
    for fencer in fencers:
        print("Fencer", fencer.id, fencer.name)

@click.command(name="addfencer")
@click.argument("name")
@with_appcontext
def add_fencer(name):
    fencer = Fencer(name=name)
    db.session.add(fencer)
    db.session.commit()
    print("Fencer added")

@click.command(name="addtournament")
@click.argument("name")
@with_appcontext
def add_tournament(name):
    tournament = Tournament(name=name)
    db.session.add(tournament)
    db.session.commit()
    print("tournament added")

@click.command(name="addftot")
@click.argument("name")
@click.argument("tournament")
@with_appcontext
def add_fencer_to_tourn(name, tournament):
    fencer = Fencer.query.filter(Fencer.name == name).first()
    tourn = Tournament.query.filter(Tournament.name == tournament).first()
    fencer.tournaments.append(tourn)
    db.session.commit()
    print("Fencer added to tournament")

@click.command(name="cleardb")
@with_appcontext
def clear_db():
    db.drop_all()
    db.session.commit()
    print("Database tables cleared, remember to recreate them!")