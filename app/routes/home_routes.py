from app import db
from app.models.movie import Movie
from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import desc
import requests
import os

API_KEY = os.environ.get("TMDB_API")

home_bp = Blueprint("home", __name__)
movie_search_url = "https://api.themoviedb.org/3/search/movie"


@home_bp.route("/", methods=["GET"])
def show_popular_movies():
    movies = []
    for i in range(1, 2):
        url = f'https://api.themoviedb.org/3/discover/movie?page={i}&sort_by=popularity.desc&api_key={API_KEY}'
        response = requests.get(url)
        movies.extend(response.json()["results"])
    return render_template("index.html", movies=movies)