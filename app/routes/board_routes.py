from flask import Blueprint, Response, request
from app.models.card import Board
from .route_utilities import validate_model, create_model
from ..db import db

bp = Blueprint("boards", __name__, url_prefix="/boards")

@bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict(), 200

@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)
