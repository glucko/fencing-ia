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
class FencerForm(FlaskForm):
    main_fencer = IntegerField(widget=HiddenInput())
    opponent = IntegerField(widget=HiddenInput())
    main_fencer_name = StringField(widget=HiddenInput())
    score = StringField('Score')
    is_different = BooleanField('is_repeat', widget=HiddenInput())

class TournamentForm(FlaskForm):
    name = StringField('name', widget=HiddenInput())
    fencers = FieldList(FormField(FencerForm))

@display_blueprint.route('/display/<int:tourn_id>', methods=['GET'])
def display(tourn_id=None):
    tournament = Tournament.query.get(tourn_id)
    fencers = tournament.fencers

    tournament_form = TournamentForm()
    tournament_form.name = tournament.name
    pairs = []
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

            if i.id == j.id:
                fencer_form.is_different = False
            tournament_form.fencers.append_entry(fencer_form)
            pairs.append(frozenset([i,j]))

    chunks = []
    chunk_len = len(fencers)
    for i in range(0, len(pairs), chunk_len):
        chunks.append(tournament_form.fencers[i:i + chunk_len])
    
    return render_template('tournament_display.html', tournament_form=tournament_form, chunks=chunks)

@display_blueprint.route('/display/<int:tourn_id>', methods=['POST'])
def update(tourn_id=None):
    #pp.pprint(request.form)

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