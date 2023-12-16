from setup import ma, db 
from marshmallow import fields
from marshmallow.validate import Regexp


# Here the League model is defined with db.Model.
# The table name "leagues" is assigned to the dunder 
# "__tablename__". All of the entitiy fields are defined
# in the class, as well as their datatypes.
class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)

    name = db.Column(db.String, unique=True)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())


    teams = db.relationship("Team", back_populates="league_id")

    # Foreign Key - establishes a relationship at the database level
    sport = db.Column(db.Integer, db.ForeignKey("sports.id"), nullable=False) # Foreign Key
    # SQLAlchemy relationship - nests an instance of a related model
    sport_id = db.relationship("Sport", back_populates="leagues")


# In the LeagueSchema class, all of the fields are defined.
# This allows client routes to verify the field names. 
class LeagueSchema(ma.Schema):

    teams = fields.List(fields.Nested(
        "TeamSchema", exclude=[
            "league_id", "date_created", "id", "users"
            ]))
    # Tell Marshmallow to nest a SportSchema instance when serialising
    sport_id = fields.Nested("SportSchema", exclude=["leagues"])

    class Meta:
        fields = ("id", "name", "start_date", "end_date", "sport_id", "teams")


class LeagueInputSchema(ma.Schema):

    name = fields.String(
        validate=Regexp("^[a-zA-Z ]+$", error="Must only contain letters and spaces."))
    start_date = fields.Date()
    end_date = fields.Date()

    teams = fields.List(fields.Nested(
        "TeamSchema", exclude=[
            "league_id", "date_created", "id", "users"
            ]))

    class Meta:
        fields = ("id", "name", "start_date", "end_date", "sport", "teams")