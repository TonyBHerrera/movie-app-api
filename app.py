from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model):
    __tablename__= "Movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    starring = db.Column(db.String(100), nullable=False)

    def __init__(self, title, year, rating, genre, starring):
        self.title = title
        self.year = year
        self.rating = rating
        self.genre = genre
        self.starring = starring
    
class MoviesSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "year", "rating", "genre", "starring")

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)

@app.route("/", methods=["GET"])
def home():
    return "<h1> Home page</h1>"


@app.route("/movies",methods=["GET"])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)
    return jsonify(result)   



@app.route("/movie/<id>", methods=["GET"])
def get_movie():
    movie = Movie.query.get(id)

    result = movie_schema.dump(movie)
    return jsonify(result)


@app.route("/movie", methods=["POST"])
def add_movie():
    title = request.json["title"]
    year = request.json["year"]
    rating = request.json["rating"]
    genre = request.json["genre"]
    starring = request.json["starring"]

    new_movie = Movie(title, year, rating, genre, starring)

    db.session.add(new_movie)
    db.session.commit()

    movie = Movie.query.get(new_movie.id)
    return movie_schema.jsonify(movie)

@app.route("/movie/<id>", methods=["PATCH"])
def update_movie(id):
    movie = Movie.query.get(id)

    new_title = request.json["title"]

    movie.title = new_title

    db.session.commit()
    return movie_schema.jsonify(movie)

@app.route("/movie/<id>", methods=["DELETE"])
def delete_movie(id):
    record = Movie.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("PEW PEW PEW she gone") 

if __name__ == "__main__":
    app.debug = True
    app.run()