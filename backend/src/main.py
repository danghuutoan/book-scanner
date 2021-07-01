from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from werkzeug.utils import secure_filename
import uuid

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
    author = db.Column(db.String)
    title = db.Column(db.String)
    pages = relationship("Page")


class Page(db.Model):
    __tablename__ = "pages"
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    content = db.Column(db.String)
    image_path = db.Column(db.String)
    book_id = db.Column(db.Integer, ForeignKey("books.id"))


@app.route("/", methods=["GET"])
def render_home_page():
    return render_template("home.html")


@app.route("/books", methods=["GET"])
def render_book_page():
    books = Book.query.all()
    print(books)
    return render_template("books.html", books=books)


@app.route("/books", methods=["POST"])
def create_new_book():
    book_tile = request.form["bookTile"]
    book_author = request.form["bookAuthor"]
    book = Book(title=book_tile, author=book_author)
    db.session.add(book)
    db.session.commit()
    return redirect("/books")


@app.route("/books/new", methods=["GET"])
def render_new_book_form():
    return render_template("new_book_form.html")


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_by_id(book_id):
    book = db.session.query(Book).get(book_id)
    if book is None:
        return {"status": "failed"}, 404

    db.session.delete(book)
    db.session.commit()
    return {"status": "ok", "id": book.id}


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    book = db.session.query(Book).get(book_id)
    if book is None:
        return {"status": "failed"}, 404

    return render_template("book.html", book=book)


@app.route("/books/<int:book_id>/pages/upload", methods=["POST"])
def upload_page(book_id):
    book = db.session.query(Book).get(book_id)
    if book is None:
        return {"status": "failed"}, 404
    f = request.files["file"]
    random_string = uuid.uuid4().hex[:6].upper()
    file_path = f"static/images/{secure_filename(random_string +f.filename)}"
    f.save(file_path)
    page = Page(book_id=book_id, image_path=file_path)
    db.session.add(page)
    db.session.commit()
    return render_template("book.html", book=book)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
