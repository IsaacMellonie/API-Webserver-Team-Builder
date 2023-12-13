from setup import app
from blueprints.cli_bp import db_commands 
from blueprints.users_bp import users_bp
from blueprints.teams_bp import teams_bp
from blueprints.leagues_bp import leagues_bp
from blueprints.sports_bp import sports_bp 


app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(leagues_bp)
app.register_blueprint(sports_bp)



