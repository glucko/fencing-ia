from flask import Blueprint, render_template, abort, redirect, url_for, current_app
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
import os

forms = Blueprint('forms', __name__,
                        template_folder='templates')

class PhotoForm(FlaskForm):
    image = FileField('image', validators=[
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
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@forms.route('/manual_entry', methods=['GET', 'POST'])
def manual_entry():
    manual_form = ManualEntry()

    if manual_form.validate_on_submit():
        return render_template('index.html')
    return render_template('manual_entry.html', form=manual_form)