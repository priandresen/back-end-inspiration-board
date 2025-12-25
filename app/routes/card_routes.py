from flask import Blueprint, Response, abort, make_response, request
from app.models.card import Card
#from .route_utilities import validate_model, create_model
from ..db import db

bp = Blueprint("cards", __name__, url_prefix="/cards")