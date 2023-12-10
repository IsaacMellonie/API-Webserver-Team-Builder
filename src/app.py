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
    bio = db.Column(db.String(200), default="Introduce yourself")
    available = db.Column(db.Boolean, default=True)
    phone = db.Column(db.Integer())
    team_id = db.Column(db.Integer())


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
    captain = db.Column(db.String(), default=None)
    league = db.Column(db.String(), default=None)
    players = db.Column(db.String(), default=None)


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1), default="League Name")
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    sport = db.Column(db.String())


class Ladder(db.Model):
    __tablename__ = "ladders"

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer())
    team = db.Column(db.String())
    points = db.Column(db.Integer(), default=0)
    win = db.Column(db.Integer(), default=0)
    loss = db.Column(db.Integer(), default=0)
    draw = db.Column(db.Integer(), default=0)
    league_id = db.Column(db.Integer())


@app.cli.command("seed")
def db_seed():
    users = [
        User(
            admin=True,
            captain=True,
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
            first="Gary",
            last="Smith",
            email="smith@email.com",
            password="pwd123",
            bio="I usually play on the wing. Not very expereinced."
        ),
        User(
            first="May",
            last="Pham",
            email="pham@email.com",
            password="pwd123",
            bio="Hi! Excited to meet everyone!"
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
            captain="John Johnson",
        ),
        Team(
            team_name="Bandits",
            captain="None",
        )
    ]
    db.session.add_all(teams)
    db.session.commit()

    leagues = [
        League(
            name="C",
            start_date="2024-01-11",
            end_date="2024-04-04",
        )
    ]
    db.session.add_all(leagues)
    db.session.commit()

    ladders = [
        Ladder(
            position=1,
        ),
        Ladder(
            position=2,
        ),
        Ladder(
            position=3,
        ),
        Ladder(
            position=4,
        ),
        Ladder(
            position=5,
        ),
        Ladder(
            position=6,
        ),
        Ladder(
            position=7,
        ),
        Ladder(
            position=8,
        ),
        Ladder(
            position=9,
        ),
        Ladder(
            position=10,
        ),
        Ladder(
            position=11,
        )
    ]
    db.session.add_all(ladders)
    db.session.commit()

    print("Database Seeded")


@app.cli.command("create")
def db_create():
    db.drop_all()
    db.create_all()
    print("Created Tables")


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/captain")
def all_users():
    # select * from users;
    # Use a comma to separate conditions. Just like the AND operator.
    # to run it through an OR operator, wrap it with db._or() function.
    # eg. stmt = db.select(User).where(db.or_(User.captain, User.team_id == 1))
    # use the .order_by() function to sort the results
    stmt = db.select(User).where(User.captain)#, User.team_id == 1)#.order_by(User.date_created) 
    users = db.session.scalars(stmt)
    for user in users:
        return user
    

@app.cli.command("non_captain")
def all_users():
    # select * from users;
    stmt = db.select(User).where(User.captain != True)
    users = db.session.scalars(stmt)
    for user in users:
        print(user.first)