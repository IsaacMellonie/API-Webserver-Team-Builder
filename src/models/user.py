from setup import db, ma
from datetime import date

# User model is defined with fields for id, admin,
# captain, date_created, first, last, dob, email, 
# password, bio, available, phone, and team_id.
# All of the users' biometric data is stored here,
# along with their login details. Users can update
# their availability each week with "available".
# User phone numbers are stored in case of game
# cancellations or last minute game changes.
# The dafault team_id value is set to 1, which
# represents free agents. These free agent players
# are then assigned to a team by an admin.
# Because of the social aspect of the app,
# a bio is included where users can let others
# know a little about themselves.
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    captain = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date(), default=date.today())
    first = db.Column(db.String, default="First", nullable=False)
    last = db.Column(db.String, default="Last", nullable=False)
    dob = db.Column(db.Date)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String(200), default="Introduce yourself")
    available = db.Column(db.Boolean, default=True)
    phone = db.Column(db.BigInteger())
    team_id = db.Column(db.Integer(), default=1)

# The UserSchema is defined here.
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "admin", "captain", "date_created",
                  "first", "last", "dob", "email", "password",
                  "bio", "available", "phone", "team_id")