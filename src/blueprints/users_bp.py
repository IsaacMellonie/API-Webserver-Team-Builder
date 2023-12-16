from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask import Blueprint, abort
from models.user import User, UserSchema
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError 
from flask import request
from flask_jwt_extended import jwt_required
from auth import admin_required, captain_required, user_id_required


# A url prefix "/users" is assigned to all routes,
# which eliminates the need for declaring the url prefix
# separatley each time. Future changes to routes will be
# alot less time consuming this way. The entity name is
# also passed in. The data is then assigned to "users_bp".
users_bp = Blueprint("users", __name__, url_prefix="/users")


# This route registers a user. The user must enter, first name, last name, email and pasword.
@users_bp.route("/", methods=["POST"])
def register_user():
    try:
        # Parse incoming POST body through the schema
        # Here the id is excluded from the request
        user_info = UserSchema(exclude=["id", "admin", "date_created", "team"]).load(request.json) 
        # Create a new user with the parsed data
        user = User(
            captain=user_info.get("captain"),
            first=user_info["first"],
            last=user_info["last"],
            dob=user_info.get("dob"), # if not provided, default to None
            email=user_info["email"],
            password=bcrypt.generate_password_hash(user_info["password"]).decode("utf8"),
            bio=user_info.get("bio", ""),
            available=user_info.get("available"),
            phone=user_info.get("phone"),
            team_id=user_info.get("team.id", 1),
        )
        # Add and commit the new user to the database
        db.session.add(user)
        # Return the new user
        db.session.commit()
        # Password is excluded from the returned data dump
        return UserSchema(exclude=["password", "team"]).dump(user), 201 
    except IntegrityError:
        return {"error": "Email address already exists"}, 409 # 409 is a conflict


# This is the login route for users
@users_bp.route("/login", methods=["POST"])
def login():
    user_info = UserSchema(exclude=["id", "admin", "date_created", "first", "last", "dob", 
                                    "bio", "available", "phone", "team"]).load(request.json)
    stmt = db.select(User).where(User.email==user_info["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        token = create_access_token(identity=user.email, expires_delta=timedelta(hours=10))
        return {"token": token, "user": UserSchema(only=["first", "last", "email", "team.id"]).dump(user)}
    else:
        return {"error": "Invalid email or password"}, 401


# Get all captains
@users_bp.route("/captains")
@jwt_required()
def captains():
    # select * from users;
    # Use a comma to separate conditions. Just like the AND operator.
    # to run it through an OR operator, wrap it with db._or() function.
    # eg. stmt = db.select(User).where(db.or_(User.captain, User.team_id == 1))
    # use the .order_by() function to sort the results
    stmt = db.select(User).where(User.captain)#, User.team_id == 1)#.order_by(User.date_created) 
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=["password", "team.league_id", 
                                          "team.users", "team.points"]).dump(users)
    

# Get Free Agents users on team id=1. This is useful for captains
# and admins who need to find players.
@users_bp.route("/freeagents")
@jwt_required()
def free_agents():
    captain_required()
    # select all users that are not assigned a team;
    stmt = db.select(User).where(db.and_(User.captain != True, User.team_id == 1))
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=["password", "team.league_id", 
                                          "team.users", "team.points"]).dump(users)


# Update the user information stored in the database.
@users_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    user_id_required(id)
    try:
        user_info = UserSchema(exclude=["id", "admin", "date_created", 
                                        "captain"]).load(request.json)
        stmt = db.select(User).filter_by(id=id)
        user = db.session.scalar(stmt)
        if user: # Add and user email == email
            # user.captain = user_info.get("captain", user.captain)
            user.first = user_info.get("first", user.first)
            user.last = user_info.get("last", user.last)
            user.dob = user_info.get("dob", user.dob)
            user.email = user_info.get("email", user.email)
            user.password = user_info.get("password", user.password)
            user.bio = user_info.get("bio", user.bio)
            user.available = user_info.get("available", user.available)
            user.phone = user_info.get("phone", user.phone)
            user.team_id = user_info.get("team_id.teams.id", user.team_id)
            db.session.commit()
            return UserSchema(exclude=["admin", "date_created",
                                       "password", "team.league_id",
                                       "team.users", "team.points" ]).dump(user)
        else:
            return {"error": "User not found"}, 404
    except IntegrityError:
        return {"error": "Email address already exists"}, 409 # 409 is a conflict
    

# Delete user from database
@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    admin_required()
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {}, 200
    else:
        return {"error": "User not found"}, 404
