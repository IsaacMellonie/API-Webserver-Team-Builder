from flask import request, abort
from sqlalchemy.exc import IntegrityError 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models.user import User, UserSchema
from models.team import Team, TeamSchema 
from models.sport import Sport, SportSchema
from models.league import League, LeagueSchema 
from setup import db, ma, app, bcrypt, jwt


def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and user.admin):
        abort(401)
    

@app.errorhandler(401)
def unauthorized(err):
    return {"error": "You are not authorised to access this resource"}


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/users/register", methods=["POST"])
def register_user():
    try:
        #Parse incoming POST body through the schema
        user_info = UserSchema(exclude=["id", "admin"]).load(request.json) #Here the id is excluded from the request
        #Create a new user with the parsed data
        user = User(
            first=user_info["first"],
            last=user_info["last"],
            dob=user_info.get("dob", "1999-01-01"), #if not provided, default to empty string
            email=user_info["email"],
            password=bcrypt.generate_password_hash(user_info["password"]).decode("utf8"),
            bio=user_info.get("bio", ""),
            available=user_info.get("available"),
            phone=user_info.get("phone")
        )
        #Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()
        #Return the new user
        return UserSchema(exclude=["password"]).dump(user), 201 #Password is excluded from the returned data dump
    except IntegrityError:
        return {"error": "Email address already exists"}, 409 #409 is a conflict


#This is the login route for users
@app.route("/users/login", methods=["POST"])
def login():
    user_info = UserSchema(exclude=["id", "admin", "date_created", "first", "last", "dob", "bio", "available", "phone", "team_id"]).load(request.json)
    stmt = db.select(User).where(User.email==user_info["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        token = create_access_token(identity=user.email, expires_delta=timedelta(hours=10))
        return {"token": token, "user": UserSchema(exclude=["password"]).dump(user)}
    else:
        return {"error": "Invalid email or password"}, 401



@app.route("/users/captains")
@jwt_required()
def captains():
    # select * from users;
    # Use a comma to separate conditions. Just like the AND operator.
    # to run it through an OR operator, wrap it with db._or() function.
    # eg. stmt = db.select(User).where(db.or_(User.captain, User.team_id == 1))
    # use the .order_by() function to sort the results
    stmt = db.select(User).where(User.captain)#, User.team_id == 1)#.order_by(User.date_created) 
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=["password"]).dump(users)
    

@app.route("/users/freeagents")
@jwt_required()
def free_agents():
    admin_required()
    # select all users that are not assigned a team;
    stmt = db.select(User).where(db.and_(User.captain != True, User.team_id == 1))
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=["password"]).dump(users)


@app.route("/teams")
@jwt_required()
def all_teams():
    stmt = db.select(Team).order_by(Team.team_name.asc()) # Displays teams in ascending order. Use .desc() to flip around.
    users = db.session.scalars(stmt).all()
    return TeamSchema(many=True).dump(users)


@app.route("/teams/register", methods=["POST"])
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


@app.route("/leagues/register", methods=["POST"])
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


@app.route("/sports/register", methods=["POST"])
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