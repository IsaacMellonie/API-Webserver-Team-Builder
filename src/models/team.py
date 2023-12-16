from setup import db, ma 
from datetime import date 
from marshmallow import fields


# The Team model contains the fields "id", "team_name",
# "date_created", "points", "win", "loss", "draw",
# and "league." A primary key is generated for "id".
# "team_name" allows the user to enter a unique name.
# The "points" field is used to store the points that
# dictate the positions of each team.
# "win", "loss" and "draw" record the team wins record.
# THe final field is a foreign key for the assigned league 
class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)

    team_name = db.Column(db.String, default="Team Name", nullable=False, unique=True)
    date_created = db.Column(db.Date, default=date.today(), nullable=False)
    points = db.Column(db.Integer, default=0)
    win = db.Column(db.Integer, default=0)
    loss = db.Column(db.Integer, default=0)
    draw = db.Column(db.Integer, default=0)
    
    # The relationship with the User model is made, then
    # backpopulates the "team" relationship.
    users = db.relationship("User", back_populates="team")

    league = db.Column(db.Integer, db.ForeignKey("leagues.id")) #Foreign Key
    league_id = db.relationship("League", back_populates="teams") 


# The Schema is defined
class TeamSchema(ma.Schema):

    users = fields.List(fields.Nested("UserSchema", exclude=[
        "id", "dob", "team", "password", "date_created", "admin",
        ]))

    league_id = fields.Nested("LeagueSchema", exclude=["sport_id"])

    class Meta:
        fields = (
            "id", "team_name", "date_created", "points", 
            "win", "loss", "draw", "league_id", "users"
            )
        


class TeamInputSchema(ma.Schema):

    users = fields.List(fields.Nested("UserSchema", exclude=[
        "id", "dob", "team", "password", "date_created", "admin",
        ]))

    class Meta:
        fields = (
            "id", "team_name", "date_created", "points", 
            "win", "loss", "draw", "league", "users"
            )