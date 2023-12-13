from models.user import User
from models.team import Team 
from models.sport import Sport
from models.league import League 
from setup import db, bcrypt
from flask import Blueprint 

# Here Blueprint is defined 
db_commands = Blueprint("db", __name__)

# This command will seed the database entities.
@db_commands.cli.command("seed")
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
        ),
        Team(
            team_name="Bandits",
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
            name="A",
            start_date="2024-01-11",
            end_date="2024-04-04",
        ),
        League(
            name="B",
            start_date="2024-01-11",
            end_date="2024-04-04",
        ),
        League(
            name="C",
            start_date="2024-01-11",
            end_date="2024-04-04",
        )
    ]
    db.session.add_all(leagues)
    db.session.commit()

    print("Database Seeded")

# This command will drop the database entities.
@db_commands.cli.command("drop")
def db_drop():
        db.drop_all()
        print("Dropped Tables")

# This command will create the database entities.
@db_commands.cli.command("create")
def db_create():
    db.create_all()
    print("Created Tables")
