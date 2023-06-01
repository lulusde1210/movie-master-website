from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/movies'
    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    from .routes.movies_routes import movies_bp
    from .routes.home_routes import home_bp
    app.register_blueprint(movies_bp)
    app.register_blueprint(home_bp)

    from app.models.movie import Movie

    return app
