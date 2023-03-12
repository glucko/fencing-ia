from flask import Blueprint, render_template, abort, redirect, url_for, current_app, flash, request
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, RadioField, DateTimeLocalField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from models import Fencer, Tournament, db
import os

forms = Blueprint('forms', __name__,
                        template_folder='templates')

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


class PhotoForm(FlaskForm):
    image = FileField('Image', validators=[
        # FileRequired(),
        # FileAllowed(['jpg', 'png', 'pdf'], 'Images!')
    ])

@forms.route('/photo_entry', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()

    print(form.validate_on_submit())
    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            current_app.root_path, 'photos', filename
        ))
        return render_template('index.html')

    return render_template('forms/photo_entry.html', form=form)


class ManualEntry(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

@forms.route('/manual_entry', methods=['GET', 'POST'])
def manual_entry():
    manual_form = ManualEntry()

    if manual_form.validate_on_submit():
        return render_template('index.html')
    return render_template('forms/manual_entry.html', form=manual_form)

@forms.route('/tournament_entry', methods=['GET'])
def tournament_entry():
    return render_template('forms/tournament_entry.html')

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
