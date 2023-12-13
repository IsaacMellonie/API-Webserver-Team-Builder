from setup import ma, db 


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1))
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    sport = db.Column(db.String())


class LeagueSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "start_date", "end_date", "sport")