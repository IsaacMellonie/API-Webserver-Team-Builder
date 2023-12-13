from setup import ma, db 


class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    max_players = db.Column(db.Integer)


class SportSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "max_players")