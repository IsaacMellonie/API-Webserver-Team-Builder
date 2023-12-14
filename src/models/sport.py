from setup import ma, db 


# The Sport model defines the columns "id", "name", and "max_players"
# using SQLAlchemy db.Model.
class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    name = db.Column(db.String, nullable=False, unique=True)
    max_players = db.Column(db.Integer)

# SportSchema defines fields with the Marshmallow Schema.
# Fields allow the client routes to retrieve data for the host.
class SportSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "max_players")