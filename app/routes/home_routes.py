from app import db
from app.models.movie import Movie
from flask import Blueprint, render_template, redirect, url_for, request
from app.models.form import CreateAddForm, CreateEditForm
from sqlalchemy import desc
import requests

API_KEY = "8dfc01d0f39f67961719588a2a74b6ac"

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def show_popular_movies():
    movies = []
    for i in range(1, 20):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={i}&sort_by=popularity.desc&api_key={API_KEY}'
        response = requests.get(url)
        movies.extend(response.json()["results"])

    return render_template("index.html", movies=movies)
