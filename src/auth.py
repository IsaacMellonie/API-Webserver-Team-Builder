from models.user import User
from flask import abort
from flask_jwt_extended import get_jwt_identity
from setup import db


# AA seperate auth module was created for storing
# functions that assist with authentication on our
# bluprint routes.

# The admin_required function allows us to modularise
# for reuse later. This function finds whether a user
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



# captain_required checks if the user, identified by JWT email,
# is a captain or admin; if not, it aborts with a 401 error,
# ensuring secure team updates.
def captain_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and (user.admin or user.captain)):
        abort(401)


# captain_id_required validates that the requesting user,
# identified by JWT email, matches the team ID and holds
# captain or admin status; if not, it aborts with a 401,
# ensuring authorized team detail updates.
def captain_id_required(id):
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user.team_id == id and (user.admin or user.captain)):
        abort(401)



# user_id_required verifies that the user, identified by JWT email
# and matching user ID, exists; otherwise, it aborts with a 401 error,
# ensuring authorized user data access.
def user_id_required(id):
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email, User.id == id)
    user = db.session.scalar(stmt)
    if not user:
        abort(401)
