from flask import Blueprint, render_template, abort, redirect, url_for, current_app, flash, request
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, RadioField, DateTimeLocalField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from models import Fencer, Tournament, db
import os

forms = Blueprint('forms', __name__,
                        template_folder='templates')

########## Tournament Selection ##########

class TournamentSelect(FlaskForm):
    tournaments = QuerySelectField('Tournaments', query_factory=lambda :
                            Tournament.query, get_label='name')

@forms.route('/tournament_select', methods=['GET', 'POST'])
def tournament_select():
    tournament_form = TournamentSelect()
    tournaments = Tournament.query.all()
    tournament_form.tournaments.choices = [(t.id, t.name) for t in tournaments]

    if request.method == 'POST':
        if tournament_form.validate_on_submit():
            tournament = tournament_form.tournaments.data
            return redirect(url_for('display.display', tourn_id=tournament.id))
    return render_template('forms/tournament_select.html', form=tournament_form)


########## Fencer Registration ##########

class FencerRegistration(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    rating = RadioField('Rating', choices=[
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('U','U')],
        validators=[DataRequired()])

@forms.route('/fencer_registration', methods=['GET', 'POST'])
def fencer_registration():
    fencer_form = FencerRegistration()

    if fencer_form.validate_on_submit():
        fencer = Fencer(
        name=fencer_form.name.data, 
        email=fencer_form.email.data, 
        rating=fencer_form.rating.data
        )
        db.session.add(fencer)
        db.session.commit()

        flash("Fencer registered successfully", "info")
        return redirect(url_for('forms.fencer_registration'))
    return render_template('forms/fencer_registration.html', form=fencer_form)

########## Tournament Registration/Creation ##########

class MultiCheckboxField(QuerySelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class TournamentRegistration(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateTimeLocalField('Date', format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    fencers = MultiCheckboxField('Fencers', query_factory=lambda :
                            Fencer.query, get_label='name')

    def validate_fencers(self, fencers):
        if len(fencers.data) < 2:
            raise ValidationError('Must have at least 2 fencers')

########## Tournament Updating ##########

@forms.route('/tournament_registration', methods=['GET', 'POST'])
def tournament_registration():
    tournament_form = TournamentRegistration()
    fencers = Fencer.query.all()
    tournament_form.fencers.choices = [(f.id, f.name) for f in fencers]

    if request.method == 'POST':
        if tournament_form.validate_on_submit():
            tournament = Tournament(
                name=tournament_form.name.data,
                date=tournament_form.date.data,
                location=tournament_form.location.data,
                fencers=tournament_form.fencers.data
            )
            # for i in tournament_form.fencers.data:
            #     tournament.fencers.append(i)
            db.session.add(tournament)
            db.session.commit()

            return redirect(url_for("display.display", tourn_id=tournament.id))

    return render_template('forms/tournament_registration.html', form=tournament_form)
