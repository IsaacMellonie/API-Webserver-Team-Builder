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


# A user can register a sport here. Sport names must be unique.
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


# Update a Sport
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
            return SportSchema(exclude=["id",]).dump(sport)
        else:
            return {"error": "Sport not found"}
    except IntegrityError:
        return {"error": "Sport already exists."}, 409 # 409 is a conflict


# Delete a Sport
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



# Get a sport by id
@sports_bp.route("/<int:id>")
@jwt_required()
def get_sport(id):
    stmt = db.select(Sport).filter_by(id=id) 
    league = db.session.scalar(stmt)
    if league:
        return SportSchema(exclude=["leagues.teams"]).dump(league)
    else:
        return {"error": "League not found"}, 404