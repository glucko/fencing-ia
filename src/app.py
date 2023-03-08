from flask import Flask, render_template
from models import db
from forms import forms
from display import display_blueprint
from cli import create_db, print_db, add_fencer, add_fencer_to_tourn, add_tournament
import os

file_path = os.path.abspath(os.getcwd())+"/tmp/test.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasdfwerqewgfgzvzxc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.cli.add_command(print_db)
app.cli.add_command(create_db)
app.cli.add_command(create_db)
app.cli.add_command(add_fencer)
app.cli.add_command(add_fencer_to_tourn)
app.cli.add_command(add_tournament)

db.init_app(app)

app.register_blueprint(forms)
app.register_blueprint(display_blueprint)

# create route
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
