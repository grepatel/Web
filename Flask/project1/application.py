# key: ijjVyBqDTn7SbA1SJJF8sw
# secret: 1G0Ja04q7q9uJbqWDfNJzH1E7RhPq6g9YUhlxowINjI

import os
from urllib.request import urlopen

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

res = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params={"key": "ijjVyBqDTn7SbA1SJJF8sw",
                           "isbns": "9781632168146"})
print(res.json())

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id") is None:
        session["user_id"] = False

    if request.method == "POST":
        user_email = request.form.get("user_email")
        user_pwd = request.form.get("user_pwd")
        user_id = db.execute(
            f"SELECT user_id FROM user_info WHERE user_email='{user_email}' AND user_pwd='{user_pwd}';").fetchone()

        session["loggedIn"] = user_id
        if session["loggedIn"] is not None:
            return render_template("booksearch.html")

        else:
            error = "Login failed. Please register if you haven't already. " \
                    "Else, please try again. "
            return render_template("login.html", error=error)

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_email = request.form.get("user_email")
        user_pwd = request.form.get("user_pwd")
        exists = db.execute(
            f"SELECT user_id FROM user_info WHERE user_email='{user_email}';").fetchone()

        if exists is None:
            db.execute(
                "INSERT INTO user_info (user_name,user_email,user_pwd) VALUES "
                "(:user_name,:user_email,:user_pwd)", {"user_name": user_name,
                                                       "user_email": user_email,
                                                       "user_pwd": user_pwd})

            db.commit()
            return render_template("booksearch.html")
        else:
            error = "This email is already registered. Please login."
            return render_template("login.html", error=error)
    else:
        return render_template("index.html")


@app.route("/booksearch", methods=["GET", "POST"])
def booksearch():
    if session.get("user_id") is None:
        return render_template("login.html")

    if request.method == "POST":
        search_text = request.form.get("search_text")
        books = db.execute(
            f"SELECT book_id,title,isbn,author,year, avg_rating FROM book WHERE isbn like '%{search_text}%' OR author "
            f"like '"
            f"%{search_text}%' OR "
            f"title like '%"
            f"{search_text}';").fetchall()
        if books is not None:
            message =  "Found matching books.."
            return render_template("booksearch.html", books=books)
        else:
            error = "No book found matching your criteria. Please try again..."
            return render_template("booksearch.html", error=error)

    else:
        return render_template("booksearch.html")


@app.route("/bookreview", methods=["GET", "POST"])
def bookreview():
    if session.get("user_id") is None:
        return render_template("login.html")

    if request.method == "GET":
        user_id = session.get("user_id")
        book_id = request.args.get("bookid")
        user_rating = request.form.get("review")
        review_text = request.form.get("review_text")

        if review_text is not None:
            success = db.execute(
                "INSERT INTO review (user_id,user_rating,user_review,book_id) VALUES "
                "(:user_id,:user_rating,:user_review,:book_id)", {"user_id": user_id, "user_rating": user_rating,
                                                                 "user_review": review_text, "book_id": book_id})

            db.commit()
            if seccess is None:
                error="Failed to submit review..."
                return  render_template("bookreview.html",error=error)
            else:
                message = "Review submitted."
                return render_template("bookreview.html",message=message)
        reviews = db.execute(f"SELECT user_review FROM review WHERE book_id={book_id}").fetchall()
        if reviews is not None:
            return render_template("bookreview.html", reviews=reviews)
        else:
            error = "Book Not found. Please try again..."
            return render_template("bookreview.html", error=error)

    else:
        return render_template("bookreview.html")


@app.route("/")
def index():
    return render_template("booksearch.html")
