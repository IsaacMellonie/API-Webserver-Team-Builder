from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import date

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://isaac:my_pwd_2023@127.0.0.1:5432/teamup"


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date(), default=date.today()) 
    captain = db.Column(db.Boolean, default=False)
    first = db.Column(db.String, default="First", nullable=False)
    last = db.Column(db.String, default="Last", nullable=False)
    dob = db.Column(db.Date)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String(200), default="Introduce yourself here. E.g. How long you've been playing.")
    available = db.Column(db.Boolean, default=False)
    phone = db.Column(db.Integer())


class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    max_players = db.Column(db.Integer)


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String, default="Team Name", nullable=False)
    date_created = db.Column(db.Date, default=date.today())
    captain = db.Column(db.String())
    league = db.Column(db.String())
    players = db.Column(db.String())
    captain_email = db.Column(db.String(60))

class League():
    __tablename__ = "leagues"

    id = db.Column(db.String(), primary_key=True)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    sport = db.Column(db.String())


class Ladder():
    __tablename__ = "ladders"

    id = db.Column(db.Integer, primary_key=True)
    positions = db.Column(db.Integer())
    points = db.Column(db.Integer())
    win = db.Column(db.Integer())
    loss = db.Column(db.Integer())
    draw = db.Column(db.Integer())
    league_id = db.Column(db.Integer())
    team = db.Column(db.String())


@app.cli.command("drop")
def db_drop():
    db.drop_all()
    print("Dropped Tables")


@app.cli.command("create")
def db_create():
    db.create_all()
    print("Created Tables")


@app.cli.command("seed")
def db_seed():
    users = [
        User(
            admin=True,
            first="John",
            last="Johnson",
            dob="1986-08-12",
            email="admin@email.com",
            password="pwd123",
            bio="Hi, I've been playing touch football for about 10 years. I play middle.",
            available=True,
            phone=1234567890,
        ),
        User(
            admin=False,
            first="Gary",
            last="Smith",
            email="smith@email.com",
            password="pwd123",
        ),
        User(
            admin=False,
            first="May",
            last="Pham",
            email="pham@email.com",
            password="pwd123",
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    sports = [
        Sport(
            name="Touch Football",
            max_players=12,
        ),
        Sport(
            name="Soccer",
            max_players=17,
        ),
        Sport(
            name="Netball",
            max_players=18,
        ),
        Sport(
            name="Softball",
            max_players=22,
        )
    ]
    db.session.add_all(sports)
    db.session.commit()

    teams = [
        Team(
            team_name="Get Plastered",
            date_created=date.today(),
            captain=
        )
    ]
    print("Database Seeded")


@app.route("/")
def index():
    return "Hello, World!"