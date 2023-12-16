from models.user import User
from models.team import Team 
from models.sport import Sport
from models.league import League 
from setup import db, bcrypt
from flask import Blueprint 

# Here Blueprint is defined 
db_commands = Blueprint("db", __name__)

# Creates a Flask CLI command db_seed to populate the database 
# with predefined data, enhancing development efficiency by 
# providing a consistent initial data state for testing and 
# development purposes.
@db_commands.cli.command("seed")
def db_seed():
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
        ),
        Sport(
            name="Basketball",
            max_players=16,
        ),
        Sport(
            name="Hockey",
            max_players=17,
        ),
        Sport(
            name="Touch Rugby",
            max_players=12,
        ),
        Sport(
            name="Volleyball",
            max_players=5,
        )
    ]
    db.session.add_all(sports)
    db.session.commit()

    leagues = [
        League(
            name="A",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[0].id,
        ),
        League(
            name="B",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[0].id,
        ),
        League(
            name="C",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[0].id,
        ),
        League(
            name="D",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[0].id,
        ),
        League(
            name="E",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[0].id,
        ),
        League(
            name="F",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[0].id,
        ),
        League(
            name="A",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[1].id,
        ),
        League(
            name="B",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[1].id,
        ),
        League(
            name="C",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[1].id,
        ),
        League(
            name="D",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[1].id,
        ),
        League(
            name="E",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[1].id,
        ),
        League(
            name="F",
            start_date="2024-01-11",
            end_date="2024-04-04",
            sport=sports[1].id,
        )
    ]
    db.session.add_all(leagues)
    db.session.commit()

    teams = [
        Team(
            team_name="Free Agents",
            points=0,
            league=leagues[0].id,
        ),
        Team(
            team_name="Get Plastered",
            points=10,
            win=5,
            loss=1,
            draw=0,
            league=leagues[0].id,
        ),
        Team(
            team_name="Bandits",
            points=4,
            win=2,
            loss=3,
            draw=0,
            league=leagues[0].id,
        ),
        Team(
            team_name="Potato Heads",
            points=7,
            win=3,
            loss=1,
            draw=1,
            league=leagues[0].id,
        ),
        Team(
            team_name="Deep Fryers",
            points=2,
            win=1,
            loss=4,
            draw=0,
            league=leagues[0].id,
        ),
        Team(
            team_name="The Gurus",
            points=9,
            win=4,
            loss=1,
            draw=1,
            league=leagues[0].id,
        ),
        Team(
            team_name="Side Steppers",
            points=6,
            win=3,
            loss=2,
            draw=0,
            league=leagues[0].id,
        ),
        Team(
            team_name="Flying X",
            points=1,
            win=0,
            loss=5,
            draw=1,
            league=leagues[0].id,
        ),
        Team(
            team_name="Ducks",
            points=11,
            win=5,
            loss=0,
            draw=1,
            league=leagues[0].id,
        ),
    ]
    db.session.add_all(teams)
    db.session.commit()

    users = [
        User(
            admin=True,
            captain=True,
            first="John",
            last="Johnson",
            dob="1986-08-12",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="Hi, I've been playing touch football for about 10 years. I play middle.",
            available=True,
            phone=123456789,
            team_id= teams[1].id,
        ),
        User(
            admin=False,
            captain=True,
            first="Jasper",
            last="Fez",
            dob="1989-02-03",
            email="feral@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="Let me at 'em.",
            available=True,
            phone=33333333,
            team_id= teams[2].id,
        ),
        User(
            admin=False,
            captain=False,
            first="Gary",
            last="Smith",
            email="smith@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="I usually play on the wing. Not very experienced.",
            available=False,
            phone=87336762,
            team_id=teams[2].id,
        ),
        User(
            first="May",
            last="Pham",
            email="pham@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="Hi! Excited to meet everyone! Here to have fun and make friends.",
            available=False,
            phone=23398343,
            team_id=teams[3].id,
        ),
        User(
            first="Steven",
            last="Williams",
            dob="1996-04-06",
            email="steve@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="Where's the beers at?",
            available=True,
            phone=51678723,
            team_id=teams[0].id,
        ),
        User(
            admin=False,
            captain=False,
            first="John",
            last="Phillips",
            dob="1983-02-04",
            email="admin2@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="Hi, I've been playing touch football on and off for 4 years.",
            available=True,
            phone=12346790,
            team_id= teams[1].id,
        ),
        User(
            admin=False,
            captain=False,
            first="Darren",
            last="Williams",
            dob="2003-02-09",
            email="daren@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="Here to meet new people",
            available=True,
            phone=33344433,
            team_id= teams[1].id,
        ),
        User(
            admin=False,
            captain=False,
            first="Sarah",
            last="Highland",
            email="sarah@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="I usually play on the wing. Not very experienced.",
            available=True,
            phone=87333322,
            team_id=teams[2].id,
        ),
        User(
            first="Sam",
            last="Taylor",
            email="sam@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="Hi everyone! Here to make friends.",
            available=False,
            phone=23399843,
            team_id=teams[3].id,
        ),
        User(
            first="Katherine",
            last="Platz",
            dob="1999-04-12",
            email="kath@email.com",
            password=bcrypt.generate_password_hash("Password123!").decode("utf8"),
            bio="Looking to make new friends.",
            available=True,
            phone=51647873,
            team_id=teams[0].id,
        ),
    ]
    db.session.add_all(users)
    db.session.commit()

    print("Database Seeded")

# Defines a Flask CLI command db_drop that uses SQLAlchemy's 
# drop_all to delete all database tables, and prints "Dropped Tables"
# to confirm the action.
@db_commands.cli.command("drop")
def db_drop():
        db.drop_all()
        print("Dropped Tables")


# db_create() initializes the database by creating tables 
# from SQLAlchemy models and prints a confirmation message, 
# streamlining database setup in Flask applications.
@db_commands.cli.command("create")
def db_create():
    db.create_all()
    print("Created Tables")
