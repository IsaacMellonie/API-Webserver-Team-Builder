from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask import Blueprint
from models.user import User, UserSchema, UserInputSchema
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError, DataError 
from flask import request
from flask_jwt_extended import jwt_required
from auth import admin_required, captain_required, user_id_required


# A url prefix "/users" is assigned to all routes,
# which eliminates the need for declaring the url prefix
# separatley each time. Future changes to routes will be
# alot less time consuming this way. The entity name is
# also passed in. The data is then assigned to "users_bp".
users_bp = Blueprint("users", __name__, url_prefix="/users")



# The register_user function in users_bp, accessible via 
# POST request, handles new user registrations. It parses 
# and validates incoming user data with UserSchema, excluding 
# certain fields. The function then creates a new User object 
# with the provided details, including securely hashed passwords, 
# and adds it to the database. Upon successful registration, 
# it returns serialized user data, excluding sensitive 
# information like passwords. The function also manages 
# data integrity and key errors, ensuring unique email addresses 
# and valid field inputs, enhancing security and data consistency 
# in user management.
@users_bp.route("/register", methods=["POST"])
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
        )
        # Add and commit the new user to the database
        db.session.add(user)
        # Return the new user
        db.session.commit()
        # Password is excluded from the returned data dump
        return UserSchema(exclude=["password"]).dump(user), 201 
    except IntegrityError:
        return {"error": "Email address already exists"}, 409 # 409 is a conflict
    except KeyError:
        return {"error": "Invalid fields"}



# The login function in users_bp, for POST requests, handles 
# user logins. It validates email and password, checks credentials 
# against the database, and if successful, generates a JWT token 
# with a 10-hour expiry. Returns a token and user details on successful 
# login. If not, it provides an error for invalid credentials or missing 
# fields, ensuring user authentication.
@users_bp.route("/login", methods=["POST"])
def login():
    try:
        user_info = UserSchema(only=["email", "password"]).load(request.json)
        stmt = db.select(User).where(User.email==user_info["email"])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, user_info["password"]):
            token = create_access_token(identity=user.email, expires_delta=timedelta(hours=10))
            return {"token": token, "user": UserSchema(only=["first", "last", "email", "team.id"]).dump(user)}
        else:
            return {"error": "Invalid email or password"}, 401
    except KeyError:
        return {"error": "Must have email and password fields"}


# The captains function in users_bp, secured with JWT authentication,
# retrieves all users who are team captains. It uses a SQLAlchemy query
# to select users where the captain field is true, executing the query to
# fetch the results. The function then serializes the captain data, excluding
# specific fields like 'password' and certain team-related attributes, and
# returns this data. This setup provides an efficient way to access and display
# captain information within the application, ensuring data security and
# streamlined access to user roles.
@users_bp.route("/captains")
@jwt_required()
def captains():
    # select * from users;
    # Use a comma to separate conditions. Just like the AND operator.
    # to run it through an OR operator, wrap it with db._or() function.
    # eg. stmt = db.select(User).where(db.or_(User.captain, User.team_id == 1))
    # use the .order_by() function to sort the results
    stmt = db.select(User).where(User.captain)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=["password", "team.league_id", 
                                          "team.users", "team.points"]).dump(users)
    

# THis route is protected by JWT 
# and accessible only to captains. It fetches users who are potential 
# free agents (not team captains and assigned to team ID 1). It uses 
# a SQLAlchemy query with conditions to select such users, then serializes 
# and returns their data, excluding fields 'password' and specific team 
# details. This function efficiently identifies available 
# players for team recruitment, providing captains and admins with crucial 
# information for team management and player selection in the application.
@users_bp.route("/freeagents")
@jwt_required()
def free_agents():
    captain_required()
    # select all users that are not assigned a team;
    stmt = db.select(User).where(db.and_(User.captain != True, User.team_id == 1))
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=["password", "team.league_id", 
                                          "team.users", "team.points"]).dump(users)


# The update_user function in users_bp, using PUT/PATCH methods and 
# secured with JWT, allows authenticated users to update their profiles. 
# It ensures data validation and handles unique email constraints, 
# updating user details in the database and returning serialized user data, 
# excluding sensitive information. This function enhances user profile 
# management, providing error handling for non-existent users and email 
# conflicts.
@users_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    user_id_required(id)
    try:
        user_info = UserInputSchema(exclude=["id", "admin", "date_created", 
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
            user.team_id = user_info.get("team_id", user.team_id)
            db.session.commit()
            return UserInputSchema(exclude=["admin", "date_created",
                                       "password"]).dump(user)
        else:
            return {"error": "User not found"}, 404
    except IntegrityError:
        return {"error": "Email address already exists"}, 409 # 409 is a conflict
    except DataError:
        return {"error": "Phone number must be 10 digits or less"}

    

# The delete_user function is secured with JWT and requiring admin 
# privileges. It allows for the deletion of a user by their id. 
# It verifies the user's existence in the database and, if found, 
# deletes and commits the change. Successful deletion returns a 200 
# status, while a non-existent user triggers a 404 error response. 
# This setup ensures secure and accurate user deletion within the 
# application.
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
