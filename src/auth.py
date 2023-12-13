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
    