from flask import Blueprint
from setup import db
from sqlalchemy.exc import IntegrityError 
from flask import request
from flask_jwt_extended import jwt_required
from models.team import Team, TeamSchema


# A url prefix "/teams" is assigned to all routes,
# which eliminates the need for declaring the url prefix
# separatley each time. Future changes to routes will be
# alot less time consuming this way. The entity name is
# also passed in. The data is then assigned to "teams_bp".
teams_bp = Blueprint("teams", __name__, url_prefix="/teams")


# Get all teams in the database
@teams_bp.route("/all_teams")
@jwt_required()
def all_teams():
    stmt = db.select(Team).order_by(Team.team_name.asc()) # Displays teams in ascending order. Use .desc() to flip around.
    users = db.session.scalars(stmt).all()
    return TeamSchema(many=True).dump(users)


# A captain can register a new team. Team names must be unique.
@teams_bp.route("/", methods=["POST"])
@jwt_required()
def register_team():
    try:
        team_info = TeamSchema(exclude=["id", "date_created", "points", "win", "loss", "draw"]).load(request.json)
        team = Team(
            team_name=team_info["team_name"],
            # date_created=["date_created"],
            # points=team_info["points"],
            # win=team_info["win"],
            # loss=team_info["loss"],
            # draw=team_info["draw"],
        )

        db.session.add(team)
        db.session.commit()

        return TeamSchema().dump(team), 201
    except IntegrityError:
        return {"error": "Team name already exists"}, 409 #409 is a conflict
    

# Here the route specifies that we are looking
# to receive an integer type identifier. The
# database can then be queried and return the
# corresponding team that matches the id.
@teams_bp.route("/<int:id>")
@jwt_required()
def one_team(id):
    stmt = db.select(Team).filter_by(id=id)
    team = db.session.scalar(stmt)
    if team:
        return TeamSchema().dump(team)
    else:
        return {"error": "Team not found"}, 404