from flask import Flask
from flask_migrate import Migrate
from flask_restful import Resource, Api

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)



@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)