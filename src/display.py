from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList, FormField, BooleanField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired
from models import Fencer, Tournament, Score, db
from pprint import PrettyPrinter

display_blueprint = Blueprint('display', __name__,
                        template_folder='templates')
pp = PrettyPrinter()

########## Form Setup ##########

class FencerForm(FlaskForm):
    main_fencer = IntegerField(widget=HiddenInput())
    opponent = IntegerField(widget=HiddenInput())
    main_fencer_name = StringField(widget=HiddenInput())
    score = StringField('Score')

    v = IntegerField(widget=HiddenInput())
    ts = IntegerField(widget=HiddenInput())
    tr = IntegerField(widget=HiddenInput())
    indicator = IntegerField(widget=HiddenInput())
    place = IntegerField(widget=HiddenInput())

    is_different = BooleanField('is_repeat', widget=HiddenInput())

class TournamentForm(FlaskForm):
    name = StringField('name', widget=HiddenInput())
    fencers = FieldList(FormField(FencerForm))

########## Display ##########

@display_blueprint.route('/display/<int:tourn_id>', methods=['GET'])
def display(tourn_id=None):
    tournament = Tournament.query.get(tourn_id)
    fencers = tournament.fencers

    tournament_form = TournamentForm()
    tournament_form.name = tournament.name

    places = {}
    
    for i in fencers:
        for j in fencers:
            score = tournament.scores.filter_by(main_fencer_id=i.id, opponent_id=j.id).first()
            fencer_form = FencerForm()

            if score is not None:
                fencer_form.score = score.score
            else:
                fencer_form.score = '0'

            fencer_form.main_fencer = i.id
            fencer_form.opponent = j.id
            fencer_form.main_fencer_name = i.name

            other = other_information(i.id)
            fencer_form.v = other[0]
            fencer_form.ts = other[1]
            fencer_form.tr = other[2]
            fencer_form.indicator = other[3]

            places[other[3]] = i.id

            if i.id == j.id:
                fencer_form.is_different = False
            tournament_form.fencers.append_entry(fencer_form)

    ### Sort by indicator to find place/ranking ###
    places = dict(sorted(places.items(), reverse=True))
    for i in tournament_form.fencers:
        i.place.data = list(places.keys()).index(i.indicator.data)+1

    ### Split into chunks for table rows and columns ###
    chunks = []
    chunk_len = len(fencers)
    for i in range(0, len(tournament_form.fencers), chunk_len):
        chunks.append(tournament_form.fencers[i:i + chunk_len])
     
    return render_template('tournament_display.html', tournament_form=tournament_form, chunks=chunks)

########## Upload Updated Tournament from Website to Database ##########

@display_blueprint.route('/display/<int:tourn_id>', methods=['POST'])
def update(tourn_id=None):
    chunks = []
    chunk_len = 3
    temp = list(request.form.items())
    for i in range(2, len(temp)-1, chunk_len):
        chunks.append(temp[i:i + chunk_len])
    pp.pprint(chunks)

    tournament = Tournament.query.get(tourn_id)
    for i in chunks:
        score = tournament.scores.filter_by(main_fencer_id=i[0][1], opponent_id=i[1][1]).first()
        if score is None:
            score = Score(tournament_id=tourn_id, main_fencer_id=i[0][1], opponent_id=i[1][1], score=i[2][1])
            tournament.scores.append(score)
        else:
            score.score = i[2][1]
        db.session.commit()
    return redirect(url_for('display.display', tourn_id=tourn_id))


########## Helper Functions ##########

def other_information(fencer_id):
    fencer = Fencer.query.get(fencer_id)
    touches_scored = Score.query.filter_by(main_fencer_id=fencer_id).all()
    touches_received = Score.query.filter_by(opponent_id=fencer_id).all()
    victory_count = 0
    ts = 0
    tr = 0

    for i in touches_scored:
        if 'V' in i.score:
            victory_count += 1
        if 'L' in i.score or 'V' in i.score:
            ts += int(i.score[1:])
        else:
            ts += int(i.score)

    for i in touches_received:
        if 'L' in i.score or 'V' in i.score:
            tr += int(i.score[1:])
        else:
            tr += int(i.score)
    indicator = ts - tr

    return (victory_count, ts, tr, indicator)