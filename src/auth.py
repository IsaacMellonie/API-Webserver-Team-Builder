from models.user import User
from flask import abort
from flask_jwt_extended import get_jwt_identity
from setup import db


# AA sperate auth module was created for storing
# functions that assist with authentication on our
# bluprint routes.

# The admin_required function allows us to modularise
# for reuse later. THis function finds whether a user
# exists and whether that users' email matches the
# the one entered.

# If the user is not an admin, the function will
# abort the operation immediately, returning 401.
def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and user.admin):
        abort(401)


# A captain level user can update team details.
def captain_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and (user.admin or user.captain)):
        abort(401)


# The id input to the url must match the user.team_id and
# the user must be a captain level user to update team details.
def captain_id_required(id):
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user.team_id == id and (user.admin or user.captain)):
        abort(401)


# User id input must match the user's id and user email must match.
def user_id_required(id):
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email, User.id == id)
    user = db.session.scalar(stmt)
    if not user:
        abort(401)