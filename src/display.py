from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList, FormField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired
from models import Fencer, Tournament
from pprint import PrettyPrinter


display_blueprint = Blueprint('display', __name__,
                        template_folder='templates')

class FencerForm(FlaskForm):
    fencer1 = IntegerField(widget=HiddenInput())
    fencer2 = IntegerField(widget=HiddenInput())
    score = StringField('Score', validators=[DataRequired()])

class TournamentForm(FlaskForm):
    fencers = FieldList(FormField(FencerForm))

@display_blueprint.route('/display/<int:tourn_id>', methods=['GET'])
def display(tourn_id=None):
    print(id)
    tournament = Tournament.query.get(tourn_id)
    fencers = tournament.fencers

    tournament_form = TournamentForm()
    pairs = []
    for i in fencers:
        for j in fencers:
            if frozenset([i,j]) in pairs:
                fencer_form = FencerForm()
                fencer_form.fencer1.data = -1
                fencer_form.fencer2.data = -1
                fencer_form.score.data = -1
                tournament_form.fencers.append_entry(fencer_form)
                pairs.append(frozenset([i,j, None]))
            elif i.id != j.id:
                fencer_form = FencerForm()
                fencer_form.fencer1.data = i.id
                fencer_form.fencer2.data = j.id
                fencer_form.score.data = 0
                tournament_form.fencers.append_entry(fencer_form)
                pairs.append(frozenset([i,j]))
        tournament_form.fencers.append_entry(fencer_form)

    chunks = []
    chunk_len = len(fencers)-1
    for i in range(0, len(pairs), chunk_len):
        chunks.append(pairs[i:i + chunk_len])
    
    pp = PrettyPrinter()
    pp.pprint(chunks)
    return render_template('index.html', tournament=tournament, tournament_form=tournament_form)