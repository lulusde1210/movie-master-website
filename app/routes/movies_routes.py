from app import db
from app.models.movie import Movie
from flask import Blueprint, render_template, redirect, url_for, request
from app.models.form import CreateAddForm, CreateEditForm
from sqlalchemy import desc
import requests

API_KEY = "8dfc01d0f39f67961719588a2a74b6ac"
movies_endpoint = "https://api.themoviedb.org/3/search/movie"
movie_detail_endpoint_base = "https://api.themoviedb.org/3/movie"
movie_image_url = "https://image.tmdb.org/t/p/w500"


movies_bp = Blueprint("movies", __name__, url_prefix="/movies")


@movies_bp.route("", methods=["GET"])
def show_all_movies():
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("show.html", movies=all_movies)


@movies_bp.route("/edit/<movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = CreateEditForm()
    movie_id = int(movie_id)
    movie = Movie.query.get(movie_id)

    if form.validate_on_submit():
        movie.rating = float(request.form["rating"])
        movie.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('movies.show_all_movies'))

    return render_template('edit.html', form=form)


@movies_bp.route("/delete/<movie_id>")
def delete(movie_id):
    movie_id = int(movie_id)
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movies.show_all_movies'))


@movies_bp.route("/add", methods=["GET", "POST"])
def add_movie():
    form = CreateAddForm()
    if form.validate_on_submit():
        params = {
            "api_key": API_KEY,
            "query": form.title.data
        }
        response = requests.get(movies_endpoint, params=params)
        movies = response.json()["results"]
        return render_template("select.html", movies=movies)

    return render_template("add.html", form=form)


@movies_bp.route("/find", methods=["GET"])
def find_movie():
    movie_api_id = request.args.get('id')

    response = requests.get(
        f"{movie_detail_endpoint_base}/{movie_api_id}?api_key={API_KEY}")
    movie = response.json()
    title = movie["title"]
    description = movie["overview"]
    year = movie["release_date"].split("-")[0]
    img_url = f"{movie_image_url}{movie['poster_path']}"

    new_movie = Movie(
        title=title,
        year=year,
        description=description,
        img_url=img_url,
    )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("movies.edit", movie_id=new_movie.id))
