from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ

# The module is initialised and assigned to
# "app".
app = Flask(__name__)


# Here the module environ is used to obtain
# "JWT_KEY" from .flaskenv. This creates a
# safer method of configuring without exposing
# sensitive data once the project is shared
# or pushed to GitHub.
app.config["JWT_SECRET_KEY"] = environ.get("JWT_KEY")


# Here the module environ is used to obtain
# "DB_URI" from .flaskenv. This creates a
# safer method of configuring without exposing
# sensitive data once the project is shared
# or pushed to GitHub.
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI")


# With  imports from SQLAlchemy, Marshmallow,
# Bcrypt and JWTManager, the app is initialised
# then assigned to four separate variables.
# These are then used throughout our program.
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Here a error handler is defined which deals with 401
# errors. (unverified requests without proper authentication)
# A custom error message is returned which is useful for the client.
@app.errorhandler(401)
def unauthorized(err):
    return {"error": "You are not authorised to access this resource"}


