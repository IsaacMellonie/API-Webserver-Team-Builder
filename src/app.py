from setup import app
from blueprints.cli_bp import db_commands 
from blueprints.users_bp import users_bp
from blueprints.teams_bp import teams_bp
from blueprints.leagues_bp import leagues_bp
from blueprints.sports_bp import sports_bp 


# All blueprint modules are imported from
# the blueprints folder and passed through
# app.register_blueprint(). "app" is initialized
# in setup with flask.
# Here db_commands references all client commands
# that drop, create, and seed the database.
app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(leagues_bp)
app.register_blueprint(sports_bp)

