from setup import ma, db 
from marshmallow import fields


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

    sport = db.Column(db.Integer, db.ForeignKey("sports.id"), nullable=False) # Foreign Key
    sport_id = db.relationship("Sport")


# In the LeagueSchema class, all of the fields are defined.
# This allows client routes to verify the field names. 
class LeagueSchema(ma.Schema):

    sport_id = fields.Nested("SportSchema")

    class Meta:
        fields = ("id", "name", "start_date", "end_date", "sport_id")