from flask import Blueprint
from ..db import db

bp = Blueprint("boards", __name__, url_prefix="/boards")