from flask import Blueprint
from setup import db
from flask import request
from flask_jwt_extended import jwt_required
from models.league import League, LeagueSchema
from sqlalchemy.exc import IntegrityError, DataError
from auth import admin_required


# A url prefix "/leagues" is assigned to all routes,
# which eliminates the need for declaring the url prefix
# separatley each time. Future changes to routes will be
# alot less time consuming this way. The entity name is
# also passed in. The data is then assigned to "leagues_bp".
leagues_bp = Blueprint("leagues", __name__, url_prefix="/leagues")


# This route allows a user to register a League. All league names must
# be unique for their sport but duplicates are allowed.
@leagues_bp.route("/", methods=["POST"])
@jwt_required()
def register_league():
    admin_required()
    
    league_info = LeagueSchema(exclude=["id"]).load(request.json)
    league = League(
        name=league_info["name"],
        start_date=league_info["start_date"],
        end_date=league_info["end_date"],
        sport=league_info["sport"]
    )

    db.session.add(league)
    db.session.commit()

    return LeagueSchema(exclude=["id"]).dump(league), 201


# Update a league
@leagues_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_league(id):
    admin_required()
    try:
        league_info = LeagueSchema(exclude=["id", "sport"]).load(request.json)
        stmt = db.select(League).filter_by(id=id)
        league = db.session.scalar(stmt)
        if league:
            league.name = league_info.get("name", league.name)
            league.start_date = league_info.get("start_date", league.start_date)
            league.end_date = league_info.get("end_date", league.end_date)
            db.session.commit()
            return LeagueSchema(exclude=["id",]).dump(league)
        else:
            return {"error": "League not found"}
    except DataError:
        return {"error": "Name length must be one character"}, 409 # 409 is a conflict
    except IntegrityError:
        return {"error": "League name already exists"}, 409


# Delete a league
@leagues_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required
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