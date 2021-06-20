from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
    )
    return response


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@db:5432/app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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


@app.route("/books", methods=["GET"])
def create_book():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
