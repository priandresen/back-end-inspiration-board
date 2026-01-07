from flask import Blueprint, Response, request
from app.models.board import Board
from app.models.card import Card
from .route_utilities import get_models_with_filters, validate_model, create_model
from ..db import db

bp = Blueprint("boards", __name__, url_prefix="/boards")


@bp.get("")
def get_all_boards():
    return get_models_with_filters(Board, request.args), 200


@bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict(), 200

@bp.get("/<board_id>/cards")
def get_cards_for_board(board_id):
    board = validate_model(Board, board_id)
    cards = [card.to_dict() for card in board.cards]
    return {"cards": cards}, 200

@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)

@bp.post("/<board_id>/cards")
def create_card_for_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    message = request_body.get("message")
    if not message:
        return {"Request body must include 'message'."}, 400
    
    new_card = Card(
        message=message,
        board_id=board.id,
        likes_count=0,
    )
    
    db.session.add(new_card)
    db.session.commit()

    return new_card.to_dict(), 201

@bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)
    db.session.delete(board)
    db.session.commit()
    return Response(status=204, mimetype="application/json")
