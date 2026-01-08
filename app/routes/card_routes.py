from flask import Blueprint, Response, request
from app.models.card import Card
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("cards", __name__, url_prefix="/cards")

@bp.get("/<card_id>")
def get_one_card(card_id):
    card = validate_model(Card, card_id)
    return card.to_dict(), 200

@bp.post("")
def create_card():
    request_body = request.get_json()
    return create_model(Card, request_body)

@bp.patch("/<card_id>/like")
def like_card(card_id):
    card = validate_model(Card, card_id)
    card.likes_count += 1
    db.session.commit()
    return card.to_dict(), 200

@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()
    return Response(status=204, mimetype="application/json")