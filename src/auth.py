from models.user import User
from flask import abort
from flask_jwt_extended import get_jwt_identity
from setup import db


def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and user.admin):
        abort(401)
    