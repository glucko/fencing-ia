from flask import Flask, render_template, request
from models import db
from cli import create_db, print_db, add_comp, add_comp_to_tourn, add_tournament
import os

file_path = os.path.abspath(os.getcwd())+"/tmp/test.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasdfwerqewgfgzvzxc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.cli.add_command(print_db)
app.cli.add_command(create_db)
app.cli.add_command(create_db)
app.cli.add_command(add_comp)
app.cli.add_command(add_comp_to_tourn)
app.cli.add_command(add_tournament)
db.init_app(app)

# create route
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        image = request.form['photo']
        print(image)
    
# run the app
if __name__ == '__main__':
    app.run(debug=True)
