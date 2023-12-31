from flask import Blueprint
from setup import db
from sqlalchemy.exc import IntegrityError, DataError
from flask import request
from flask_jwt_extended import jwt_required
from models.team import Team, TeamSchema, TeamInputSchema
from auth import captain_required, admin_required, captain_id_required


# A url prefix "/teams" is assigned to all routes,
# which eliminates the need for declaring the url prefix
# separatley each time. Future changes to routes will be
# alot less time consuming this way. The entity name is
# also passed in. The data is then assigned to "teams_bp".
teams_bp = Blueprint("teams", __name__, url_prefix="/teams")


# All_teams, in the teams_bp Blueprint, 
# is accessible to users with JWT authentication. It queries 
# the database to retrieve all team records, sorting them in 
# ascending order by their names. The SQLAlchemy statement, 
# db.select(Team).order_by(Team.team_name.asc()), is executed 
# to fetch the team data. The results are then serialized using 
# TeamSchema, intentionally excluding the 'league_id' and 'users' 
# fields. The function returns a JSON response containing the 
# serialized list of teams, providing a user-friendly and efficient 
# way to access comprehensive team information within the application.
@teams_bp.route("/")
@jwt_required()
def all_teams():
    stmt = db.select(Team).order_by(Team.team_name.asc())
    users = db.session.scalars(stmt).all()
    return TeamSchema(many=True, exclude=["league_id", "users"]).dump(users)


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
        return TeamSchema(exclude=["league_id"]).dump(team)
    else:
        return {"error": "Team not found"}, 404


# The register_team function in teams_bp, accessible via POST and 
# secured with JWT and captain-level access, creates a new team. 
# It validates input with TeamSchema, excluding certain fields, and 
# adds the team to the database. On successful registration, 
# it returns serialized team data with a 201 status. The function 
# also handles unique name conflicts, providing an error 
# message if the team name already exists.
@teams_bp.route("/", methods=["POST"])
@jwt_required()
def register_team():
    captain_required()
    try:
        team_info = TeamSchema(exclude=["id", "date_created", "points", "win", "loss", "draw"]).load(request.json)
        team = Team(
            team_name=team_info["team_name"])

        db.session.add(team)
        db.session.commit()

        return TeamSchema(exclude=["users"]).dump(team), 201
    except IntegrityError:
        return {"error": "Team name already exists"}, 409 #409 is a conflict
    

# The update_team function in teams_bp, for PUT and PATCH requests 
# and secured with JWT, allows a team's captain to update team details. 
# It loads and validates input data using TeamInputSchema, executes a 
# query to find the team by id, and updates attributes if the team exists. 
# The function commits changes to the database and returns updated team data. 
# It handles errors related to league validity, team name uniqueness, and 
# data types for team statistics, ensuring accurate and secure data updates.
@teams_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_team(id):
    captain_id_required(id)
    try:
        team_info = TeamInputSchema(exclude=["id", "date_created"]).load(request.json)
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
            return TeamInputSchema(exclude=["id", "users"]).dump(team)
        else:
            return {"error": "Team not found"}
    except IntegrityError:
        return {"error": "Enter a valid league and unique team name."}, 409 # 409 is a conflict
    except DataError:
        return {"error": "Integers only for points, win, loss, and draw."}, 409 # 409 is a conflict


# The delete_team function in the teams_bp Blueprint, designated 
# for DELETE requests and secured with JWT and admin-only access, 
# handles the deletion of a team based on its id. It queries the 
# database to locate the specified team and, if found, deletes it 
# from the database, committing the changes. A successful deletion 
# results in an empty response with a 200 status code. If the team 
# is not found, the function returns an error message "team not found", 
# ensuring a secure mechanism for team removal in the application.
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
    