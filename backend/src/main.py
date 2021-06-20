from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@db:5432/app"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.String)
    title = db.Column(db.String)


class Page(db.Model):
    __tablename__ = "pages"
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    content = db.Column(db.String)
    image_path = db.Column(db.String)


@app.route("/")
def hello_world():
    return "Hello, World!"

