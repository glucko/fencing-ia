from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, FieldList, FormField, BooleanField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired
from models import Fencer, Tournament
from pprint import PrettyPrinter


display_blueprint = Blueprint('display', __name__,
                        template_folder='templates')

class FencerForm(FlaskForm):
    main_fencer = IntegerField(widget=HiddenInput())
    opponent = IntegerField(widget=HiddenInput())
    main_fencer_name = StringField(widget=HiddenInput())
    score = StringField('Score', default="0")
    is_different = BooleanField('is_repeat', widget=HiddenInput())

class TournamentForm(FlaskForm):
    name = StringField('name', widget=HiddenInput())
    fencers = FieldList(FormField(FencerForm))

@display_blueprint.route('/display/<int:tourn_id>', methods=['GET'])
def display(tourn_id=None):
    print(id)
    tournament = Tournament.query.get(tourn_id)
    fencers = tournament.fencers

    tournament_form = TournamentForm()
    tournament_form.name = tournament.name
    pairs = []
    x = 0
    for i in fencers:
        for j in fencers:
            x+= 1
            fencer_form = FencerForm()
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
        chunks.append(tournament_form.fencers.data[i:i + chunk_len])
    
    pp = PrettyPrinter(compact=True, sort_dicts=False)
    pp.pprint(chunks)
    print(len(chunks[0]))
    return render_template('tournament_display.html', tournament_form=tournament_form, chunks=chunks)