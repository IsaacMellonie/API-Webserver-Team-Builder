from setup import ma, db 
from marshmallow import fields
from marshmallow.validate import Regexp


# The Sport class is an SQLAlchemy model that represents sports with 
# unique IDs, names, and maximum player counts. It includes a 
# relationship with the League model, enabling database level 
# linkage and cascade delete operations.
class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)

    name = db.Column(db.String, nullable=False, unique=True)
    max_players = db.Column(db.Integer)

    leagues = db.relationship("League", back_populates="sport_id", cascade="all, delete")


# The SportSchema class uses Marshmallow to define validation for 
# sports data, including name and max players. It also serializes 
# related league data, excluding the sport_id, facilitating data 
# exchange between client routes and the host.
class SportSchema(ma.Schema):

    name = fields.String(validate=Regexp("^[a-zA-Z ]+$", error="Must only contain letters and spaces."))
    max_players = fields.Integer(error="Must only be numbers")
    leagues = fields.List(fields.Nested("LeagueSchema", exclude=["sport_id"]))

    class Meta:
        fields = ("id", "name", "max_players", "leagues")