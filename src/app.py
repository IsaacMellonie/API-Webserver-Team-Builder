from flask import abort
from flask_jwt_extended import get_jwt_identity
from models.user import User
from setup import db, ma, app, bcrypt, jwt
from blueprints.cli_bp import db_commands 
from blueprints.users_bp import users_bp
from blueprints.teams_bp import teams_bp
from blueprints.leagues_bp import leagues_bp
from blueprints.sports_bp import sports_bp 


def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and user.admin):
        abort(401)
    

@app.errorhandler(401)
def unauthorized(err):
    return {"error": "You are not authorised to access this resource"}


app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(leagues_bp)
app.register_blueprint(sports_bp)



