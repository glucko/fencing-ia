from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


display_blueprint = Blueprint('display', __name__,
                        template_folder='templates')

@display_blueprint.route('/display/<int:tourn_id>', methods=['GET'])
def display(tourn_id=None):
    print(id)
    return render_template('index.html')