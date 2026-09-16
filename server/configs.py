from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)
db_url = os.getenv("DATABASE_URL", "sqlite:///app.db" )
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")

#jwt_secret_key = os.getenv("JWT_SECRET_KEY")
#if not jwt_secret_key:
#    raise RuntimeError("error: JWT secret key not set")

app.secret_key = 'treasureeeeeee'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy()
db.init_app(app)

bcrypt = Bcrypt(app)

api = Api(app)

