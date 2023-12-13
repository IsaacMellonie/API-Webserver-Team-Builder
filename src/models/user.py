from setup import db, ma 
from datetime import date 


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
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


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "admin", "captain", "date_created", "first", "last", "dob", "email", "password", "bio", "available", "phone", "team_id")