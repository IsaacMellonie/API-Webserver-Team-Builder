from flask import Blueprint
from setup import db
from sqlalchemy.exc import IntegrityError 
from flask import request
from flask_jwt_extended import jwt_required
from models.sport import Sport, SportSchema
from auth import admin_required


# A url prefix "/sports" is assigned to all routes,
# which eliminates the need for declaring the url prefix
# separatley each time. Future changes to routes will be
# alot less time consuming this way. The entity name is
# also passed in. The data is then assigned to "sports_bp".
sports_bp = Blueprint("sports", __name__, url_prefix="/sports")


# This Flask route, register_sport, under sports_bp, is for
# POST requests and requires JWT for authentication and
# admin privileges for access. It registers a new sport,
# using a schema for data validation and handling the addition
# to the database. The function commits the new sport entry and
# returns a 201 status on success. It also includes error
# handling for unique name constraints, returning an
# error message if a sport with the same name already exists.
@sports_bp.route("/", methods=["POST"])
@jwt_required()
def register_sport():
    try:
        admin_required()
        sport_info = SportSchema(exclude=["id"]).load(request.json)
        sport = Sport(
            name=sport_info["name"],
            max_players=sport_info["max_players"]
        )

        db.session.add(sport)
        db.session.commit()

        return SportSchema(exclude=["id"]).load(request.json), 201
    except IntegrityError:
        return {"error": "Sport name already exists"} 


# Update_sport, under sports_bp, is set up for PUT 
# and PATCH methods, secured with JWT and admin access. It updates an 
# existing sport's details based on the provided ID. The function employs 
# a schema for input validation and checks for the existence of the sport 
# before updating. On successful update, it commits changes to the database 
# and returns updated sport data. It handles cases where the sport doesn't 
# exist or when the updated name conflicts with an existing sport, providing 
# appropriate error messages.
@sports_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_sport(id):
    admin_required()
    try:
        sport_info = SportSchema(exclude=["id"]).load(request.json)
        stmt = db.select(Sport).filter_by(id=id)
        sport = db.session.scalar(stmt)
        if sport:
            sport.name = sport_info.get("name", sport.name)
            sport.max_players = sport_info.get("max_players", sport.max_players)
            db.session.commit()
            return SportSchema(exclude=["id", "leagues"]).dump(sport)
        else:
            return {"error": "Sport not found"}
    except IntegrityError:
        return {"error": "Sport already exists."}, 409


# This Flask route, delete_sport, in the sports_bp Blueprint, 
# is designated for DELETE requests and requires both JWT authentication 
# and admin rights. It aims to delete a specific sport identified by its id. 
# The function first retrieves the sport using SQLAlchemy, checks if it exists, 
# and if so, deletes it from the database, committing the changes. A successful 
# deletion returns an empty response with a 200 status code. If the sport is 
# not found, it returns an error message stating "Sport not found". This setup 
# ensures secure and precise deletion of sport records from the database.
@sports_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_sport(id):
    admin_required()
    stmt = db.select(Sport).filter_by(id=id)
    sport = db.session.scalar(stmt)
    if sport:
        db.session.delete(sport)
        db.session.commit()
        return {}, 200
    else:
        return {"error": "Sport not found"}


# This function, get_sport, secured with JWT authentication, 
# retrieves a sport by its id using SQLAlchemy. It performs 
# a database query to find the specified sport. If found, the 
# sport's details are serialized, excluding related league teams, 
# and returned. If the sport is not found, it returns an error 
# message "League not found" with a 404 status code. This approach 
# ensures secure access and accurate data retrieval, providing 
# clear feedback for both successful and unsuccessful queries.
@sports_bp.route("/<int:id>")
@jwt_required()
def get_sport(id):
    stmt = db.select(Sport).filter_by(id=id) 
    league = db.session.scalar(stmt)
    if league:
        return SportSchema(exclude=["leagues.teams"]).dump(league)
    else:
        return {"error": "League not found"}, 404