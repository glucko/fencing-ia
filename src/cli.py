import click
from flask.cli import with_appcontext
from models import Tournament, Competitor, db


@click.command(name="createdb")
@with_appcontext
def create_db():
    db.create_all()
    db.session.commit()
    print("Database tables created")

@click.command(name="printdb")
@with_appcontext
def print_db():
    users = Tournament.query.all()

    for user in users:
        print(user.id, user.name)

@click.command(name="addcompetitor")
@click.argument("name")
@with_appcontext
def add_comp(name):
    competitor = Competitor(name=name)
    db.session.add(competitor)
    db.session.commit()
    print("Competitor added")

@click.command(name="addctot")
@click.argument("name")
@click.argument("tournament")
@with_appcontext
def add_comp_to_tourn(name, tournament):
    comp = Competitor.query.filter(Competitor.name == name).first()
    tourn = Tournament.query.filter(Tournament.name == tournament).first()
    comp.tournaments.append(tourn)
    db.session.commit()
    print("Competitor added")

@click.command(name="cleardb")
@with_appcontext
def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()