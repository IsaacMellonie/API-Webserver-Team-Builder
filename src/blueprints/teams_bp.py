from flask import Blueprint
from setup import db
from sqlalchemy.exc import IntegrityError, DataError
from flask import request
from flask_jwt_extended import jwt_required
from models.team import Team, TeamSchema
from auth import captain_required, admin_required, captain_id_required


# A url prefix "/teams" is assigned to all routes,
# which eliminates the need for declaring the url prefix
# separatley each time. Future changes to routes will be
# alot less time consuming this way. The entity name is
# also passed in. The data is then assigned to "teams_bp".
teams_bp = Blueprint("teams", __name__, url_prefix="/teams")


# Get all teams in the database
@teams_bp.route("/teams")
@jwt_required()
def all_teams():
    stmt = db.select(Team).order_by(Team.team_name.asc()) # Displays teams in ascending order. Use .desc() to flip around.
    users = db.session.scalars(stmt).all()
    return TeamSchema(many=True, exclude=["league_id.teams", "users"]).dump(users)


# Register a Team
# A captain can register a new team. Team names must be unique.
@teams_bp.route("/", methods=["POST"])
@jwt_required()
def register_team():
    captain_required()
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
    

# Get a Team
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
        # The TeamSchema is returned and league_id.teams is excluded
        return TeamSchema(exclude=["league_id.teams"]).dump(team)
    else:
        return {"error": "Team not found"}, 404
    

# Update a Team
@teams_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_team(id):
    captain_id_required(id)
    try:
        team_info = TeamSchema(exclude=["id", "date_created"]).load(request.json)
        stmt = db.select(Team).filter_by(id=id)
        team = db.session.scalar(stmt)
        if team:
            team.team_name = team_info.get("team_name", team.team_name)
            team.points = team_info.get("points", team.points)
            team.win = team_info.get("win", team.win)
            team.loss = team_info.get("loss", team.loss)
            team.draw = team_info.get("draw", team.draw)
            team.league = team_info.get("league", team.league)
            db.session.commit()
            return TeamSchema(exclude=["id",]).dump(team)
        else:
            return {"error": "Team not found"}
    except IntegrityError:
        return {"error": "Team already exists."}, 409 # 409 is a conflict
    except DataError:
        return {"error": "Integers only for points, win, loss, and draw."}, 409 # 409 is a conflict


# Delete a team
@teams_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_team(id):
    admin_required()
    stmt = db.select(Team).filter_by(id=id)
    team = db.session.scalar(stmt)
    if team:
        db.session.delete(team)
        db.session.commit()
        return {}, 200
    else:
        return {"error": "team not found"}
    