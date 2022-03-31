from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.db import Session
from app.db.models import Movie, Review, User

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='kinoapp', template_mode='bootstrap3')
# Add administrative views here

admin.add_view(ModelView(User, Session))
admin.add_view(ModelView(Movie, Session))
admin.add_view(ModelView(Review, Session))
