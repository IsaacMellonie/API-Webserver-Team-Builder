from setup import ma, db 
from marshmallow import fields


# The Sport model defines the columns "id", "name", and "max_players"
# using SQLAlchemy db.Model.
class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)

    name = db.Column(db.String, nullable=False, unique=True)
    max_players = db.Column(db.Integer)

    leagues = db.relationship("League", back_populates="sport_id",)

# SportSchema defines fields with the Marshmallow Schema.
# Fields allow the client routes to retrieve data for the host.
class SportSchema(ma.Schema):

    leagues = fields.List(fields.Nested("LeagueSchema", exclude=["sport_id"]))

    class Meta:
        fields = ("id", "name", "max_players", "leagues")