from flask import Blueprint
from setup import db
from flask import request
from flask_jwt_extended import jwt_required
from models.league import League, LeagueSchema, LeagueInputSchema
from sqlalchemy.exc import IntegrityError, DataError
from auth import admin_required


# By defining this Blueprint, all routes and view 
# functions related to 'leagues' are grouped under a single entity. 
# This not only organizes the code better but also allows for scalability 
# and maintainability, especially in larger applications where 
# functionalities are divided into different sections. 
leagues_bp = Blueprint("leagues", __name__, url_prefix="/leagues")


# The Register League uses the POST method and is secured 
# with JWT authentication. It facilitates the registration of a new 
# league. Admin privileges are required for access. The function 
# uses SQLAlchemy for database operations and a schema for request 
# data validation and serialization. It creates a new League object 
# with provided details and adds it to the database. Upon successful 
# creation, it returns the serialized league data with a 201 status 
# code. The route includes error handling for data integrity issues, 
# ensuring uniqueness of league names and validity of sport IDs, and 
# provides clear feedback in case of errors.
@leagues_bp.route("/", methods=["POST"])
@jwt_required()
def register_league():
    try:
        admin_required()
        
        league_info = LeagueInputSchema(exclude=["id"]).load(request.json)
        league = League(
            name=league_info["name"],
            start_date=league_info["start_date"],
            end_date=league_info["end_date"],
            sport=league_info["sport"]
        )

        db.session.add(league)
        db.session.commit()

        return LeagueInputSchema(exclude=["id"]).dump(league), 201
    except IntegrityError:
        return {"error": "Enter a unique league name and valid sport id"}


# Update League is accessible via PUT and PATCH methods and protected 
# with JWT and admin access. It manages the update of league details. 
# It utilizes SQLAlchemy for database operations and deserializes 
# request data with a schema, ensuring data integrity. The function 
# updates league attributes only if the league exists, with error handling 
# for data and integrity errors, committing changes to the database and 
# returning updated league information. It's designed for secure data 
# modification, adhering to RESTful standards and providing clear 
# user feedback.
@leagues_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_league(id):
    admin_required()
    try:
        league_info = LeagueInputSchema(exclude=["id"]).load(request.json)
        stmt = db.select(League).filter_by(id=id)
        league = db.session.scalar(stmt)
        if league:
            league.name = league_info.get("name", league.name)
            league.start_date = league_info.get("start_date", league.start_date)
            league.end_date = league_info.get("end_date", league.end_date)
            league.sport =league_info.get("sport", league.sport)
            db.session.commit()
            return LeagueInputSchema(exclude=["id", "teams"]).dump(league)
        else:
            return {"error": "League not found"}
    except DataError:
        return {"error": "Name length must be one character"}, 409
    except IntegrityError:
        return {"error": "Enter a unique league name and valid sport id"}


# This Flask route, secured by JWT authentication and admin access control, 
# handles the deletion of a league entity by its ID using SQLAlchemy's ORM 
# for database interaction. It checks for the existence of the league before 
# deletion and commits the changes to the database, ensuring error handling 
# and adherence to RESTful principles. The function is designed for maintainability, 
# security, and effective response management, providing clear feedback to the user 
# based on the operation's outcome.
@leagues_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_league(id):
    admin_required()
    stmt = db.select(League).filter_by(id=id)
    league = db.session.scalar(stmt)
    if league:
        db.session.delete(league)
        db.session.commit()
        return {}, 200
    else:
        return {"error": "League not found"}


# This route is secured with JWT authentication and handles retrieving a 
# league's details by its ID using SQLAlchemy. The function executes a 
# database query to find the specified league and, if found, returns its 
# serialized data. If not, it returns an error message with a 404 status, 
# indicating the league was not found. It's designed for straightforward data 
# retrieval, ensuring secure access and providing clear feedback for both 
# successful and unsuccessful requests, adhering to RESTful API principles.
@leagues_bp.route("/<int:id>")
@jwt_required()
def get_league(id):
    stmt = db.select(League).filter_by(id=id)
    league = db.session.scalar(stmt)
    if league:
        return LeagueSchema().dump(league)
    else:
        return {"error": "League not found"}, 404