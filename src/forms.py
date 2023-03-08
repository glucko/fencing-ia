from flask import Blueprint, render_template, abort, redirect, url_for, current_app, flash
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
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
        print(fencer_form.name.data)
        flash("Fencer registered successfully", "info")
        return redirect(url_for('forms.fencer_registration'))
    return render_template('fencer_registration.html', form=fencer_form)


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

    return render_template('photo_entry.html', form=form)


class ManualEntry(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

@forms.route('/manual_entry', methods=['GET', 'POST'])
def manual_entry():
    manual_form = ManualEntry()

    if manual_form.validate_on_submit():
        return render_template('index.html')
    return render_template('manual_entry.html', form=manual_form)

@forms.route('/tournament_entry', methods=['GET'])
def tournament_entry():
    return render_template('tournament_entry.html')