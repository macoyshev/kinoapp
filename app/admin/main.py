from flask import Flask
from flask_admin import Admin
from sqlalchemy.orm import scoped_session

from app.admin.views import MovieModel, ReviewModel, UserView
from app.db import Session, create_bd
from app.db.models import Movie, Review, User


def create_admin() -> Flask:
    app = Flask(__name__)
    app.secret_key = 'super secret key'

    create_bd()

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='kinoapp', template_mode='bootstrap3')

    admin.add_view(UserView(User, scoped_session(Session)))
    admin.add_view(MovieModel(Movie, scoped_session(Session)))
    admin.add_view(ReviewModel(Review, scoped_session(Session)))

    return app
