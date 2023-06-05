from app import db
from app.models.movie import Movie
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models.form import CreateAddForm, CreateEditForm
import requests
import os
from sqlalchemy import desc, asc

API_KEY = os.environ.get("TMDB_API")
movie_search_url = "https://api.themoviedb.org/3/search/movie"
movie_detail_url = "https://api.themoviedb.org/3/movie"
movie_image_url = "https://image.tmdb.org/t/p/w500"
movie_video_url = "https://api.themoviedb.org/3/movie"


movies_bp = Blueprint("movies", __name__, url_prefix="/movies")


@movies_bp.route("", methods=["GET"])
def show_my_movies():
    all_movies = Movie.query.order_by(desc(Movie.rating)).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = i+1
    db.session.commit()
    return render_template("show.html", movies=all_movies)


@movies_bp.route("/detail", methods=["GET"])
def show_one_movie():
    movie_api_id = request.args.get('id')
    info_url = f"{movie_detail_url}/{movie_api_id}?api_key={API_KEY}"
    video_url = f"{movie_video_url}/{movie_api_id}/videos?api_key={API_KEY}"

    response = requests.get(info_url)
    movie = response.json()
    video_response = requests.get(video_url)
    try:
        video_id = video_response.json()["results"][-1]["key"]
    except IndexError:
        video_id = None

    video_path = f"https://www.youtube.com/embed/{video_id}"
    return render_template("detail.html", movie=movie, video_path=video_path)


@movies_bp.route("/search", methods=["GET", "POST"])
def search_movie():
    form = CreateAddForm()
    if form.validate_on_submit():
        params = {
            "api_key": API_KEY,
            "query": form.title.data
        }
        response = requests.get(movie_search_url, params=params)
        movies = response.json()["results"]
        return render_template("select.html", movies=movies)

    return render_template("search.html", form=form)


@movies_bp.route("/find", methods=["GET"])
def find_movie():
    movie_api_id = request.args.get('id')
    url = f"{movie_detail_url}/{movie_api_id}?api_key={API_KEY}"

    response = requests.get(url)
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

    try:
        db.session.add(new_movie)
        db.session.commit()
    except:
        flash(
            f"{new_movie.title} is already in your movie list, add anther movie!", 'danger')
        return redirect(url_for("home.show_all_movies"))

    return redirect(url_for("movies.edit", movie_id=new_movie.id))


@movies_bp.route("/edit/<movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = CreateEditForm()
    movie_id = int(movie_id)
    movie = Movie.query.get(movie_id)

    if form.validate_on_submit():
        movie.rating = float(request.form["rating"])
        movie.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('movies.show_my_movies'))

    return render_template('edit.html', form=form)


@movies_bp.route("/delete/<movie_id>")
def delete(movie_id):
    movie_id = int(movie_id)
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movies.show_my_movies'))
