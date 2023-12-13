from flask import Blueprint
from setup import db
from flask import request
from flask_jwt_extended import jwt_required
from models.league import League, LeagueSchema

# A url prefix "/leagues" is assigned to all routes,
# which eliminates the need for declaring the url prefix
# separatley each time. Future changes to routes will be
# alot less time consuming this way. The entity name is
# also passed in. The data is then assigned to "leagues_bp".
leagues_bp = Blueprint("leagues", __name__, url_prefix="/leagues")


# This route allows a user to register a League. All league names must
# be unique for their sport but duplicates are allowed.
@leagues_bp.route("/register", methods=["POST"])
@jwt_required()
def register_league():
    # admin_required()
    
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