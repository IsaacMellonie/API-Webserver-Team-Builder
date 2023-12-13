from flask import Blueprint
from setup import db
from sqlalchemy.exc import IntegrityError 
from flask import request
from flask_jwt_extended import jwt_required
from models.sport import Sport, SportSchema


sports_bp = Blueprint("sports", __name__, url_prefix="/sports")


@sports_bp.route("/sports/register", methods=["POST"])
@jwt_required()
def register_sport():
    try:
        # admin_required()
        
        sport_info = SportSchema(exclude=["id"]).load(request.json)
        sport = Sport(
            name=sport_info["name"],
            max_players=sport_info["max_players"]
        )

        db.session.add(sport)
        db.session.commit()

        return SportSchema(exclude=["id"]).load(request.json), 201
    except IntegrityError:
        return {"error": "Sport name already exists"}