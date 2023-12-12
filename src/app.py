from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy 
from datetime import date
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://isaac:my_pwd_2023@127.0.0.1:5432/teamup"


db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    captain = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date(), default=date.today()) 
    first = db.Column(db.String, default="First", nullable=False)
    last = db.Column(db.String, default="Last", nullable=False)
    dob = db.Column(db.Date)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String(200), default="Introduce yourself")
    available = db.Column(db.Boolean, default=False)
    phone = db.Column(db.BigInteger())
    team_id = db.Column(db.Integer(), default=1) 


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "admin", "captain", "date_created", "first", "last", "dob", "email", "password", "bio", "available", "phone", "team_id")


class Sport(db.Model):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    max_players = db.Column(db.Integer)


class SportSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "max_players")


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String, default="Team Name", nullable=False, unique=True)
    date_created = db.Column(db.Date, default=date.today())
    captain = db.Column(db.String(), default=None)
    league = db.Column(db.String(), default=None)
    players = db.Column(db.String(), default=None)


class TeamSchema(ma.Schema):
    class Meta:
        fields = ("id", "team_name", "date_created", "captain", "league", "players")


class League(db.Model):
    __tablename__ = "leagues"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(1), default="League Name", unique=True)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    sport = db.Column(db.String())


class LeagueSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "start_date", "end_date", "sport")


class Ladder(db.Model):
    __tablename__ = "ladders"

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer(), unique=True)
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
            password=bcrypt.generate_password_hash("pwd123").decode("utf8"),
            bio="Hi, I've been playing touch football for about 10 years. I play middle.",
            available=True,
            phone=1234567890,
        ),
        User(
            captain=True,
            first="Gary",
            last="Smith",
            email="smith@email.com",
            password=bcrypt.generate_password_hash("pwd123").decode("utf8"),
            bio="I usually play on the wing. Not very experienced.",
            available=False,
            phone=8733676222,
        ),
        User(
            first="May",
            last="Pham",
            email="pham@email.com",
            password=bcrypt.generate_password_hash("pwd123").decode("utf8"),
            bio="Hi! Excited to meet everyone! Here to have fun and make friends.",
            available=False,
            phone=2331983423,
        ),
        User(
            first="Steven",
            last="Williams",
            dob="1996-04-06",
            email="steve@email.com",
            password=bcrypt.generate_password_hash("pwd123").decode("utf8"),
            bio="Pretty new to the game. Here to learn.",
            available=True,
            phone=5164787923,
        ),
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
            team_name="Free Agents"
        ),
        Team(
            team_name="Get Plastered",
            captain="John Johnson",
        ),
        Team(
            team_name="Bandits",
            captain="Gary Smith"
        ),
        Team(
            team_name="Potato Heads",
        ),
        Team(
            team_name="Deep Fryers",
        ),
        Team(
            team_name="The Gurus",
        ),
        Team(
            team_name="Side Steppers",
        ),
        Team(
            team_name="Flying X",
        ),
        Team(
            team_name="Ducks",
        ),
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


@app.cli.command("drop")
def db_drop():
        db.drop_all()
        print("Dropped Tables")


@app.cli.command("create")
def db_create():
    db.create_all()
    print("Created Tables")


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/users/register", methods=["POST"])
def register():
    #Parse incoming POST body through the schema
    user_info = UserSchema(exclude=["id"]).load(request.json) #Here the id is excluded from the request
    #Create a new user with the parsed data
    user = User(
        first=user_info["first"],
        last=user_info["last"],
        dob=user_info.get("dob", "1999-01-01"), #if not provided, default to empty string
        email=user_info["email"],
        password=bcrypt.generate_password_hash(user_info["password"]).decode("utf8"),
        bio=user_info.get("bio", ""),
        available=user_info.get("available", False),
        phone=user_info.get("phone", 9292752473)
    )
    #Add and commit the new user to the database
    db.session.add(user)
    db.session.commit()
    #Return the new user
    return UserSchema(exclude=["password"]).dump(user), 201 #Password is excluded from the returned data dump


@app.route("/users/captains")
def captains():
    # select * from users;
    # Use a comma to separate conditions. Just like the AND operator.
    # to run it through an OR operator, wrap it with db._or() function.
    # eg. stmt = db.select(User).where(db.or_(User.captain, User.team_id == 1))
    # use the .order_by() function to sort the results
    stmt = db.select(User).where(User.captain)#, User.team_id == 1)#.order_by(User.date_created) 
    users = db.session.scalars(stmt)
    return UserSchema(many=True).dump(users)
    

@app.route("/users/freeagents")
def free_agents():
    # select all users that are not assigned a team;
    stmt = db.select(User).where(db.and_(User.captain != True, User.team_id == 1))
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True).dump(users)


@app.route("/teams")
def all_teams():
    stmt = db.select(Team).order_by(Team.team_name.asc()) # Displays teams in ascending order. Use .desc() to flip around.
    users = db.session.scalars(stmt).all()
    return TeamSchema(many=True).dump(users)