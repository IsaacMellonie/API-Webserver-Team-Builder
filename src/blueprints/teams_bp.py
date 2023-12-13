from flask import Blueprint
from setup import db
from sqlalchemy.exc import IntegrityError 
from flask import request
from flask_jwt_extended import jwt_required
from models.team import Team, TeamSchema


teams_bp = Blueprint("teams", __name__, url_prefix="/teams")


@teams_bp.route("/teams")
@jwt_required()
def all_teams():
    stmt = db.select(Team).order_by(Team.team_name.asc()) # Displays teams in ascending order. Use .desc() to flip around.
    users = db.session.scalars(stmt).all()
    return TeamSchema(many=True).dump(users)


@teams_bp.route("/register", methods=["POST"])
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