import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from app.models.card import Card
from app.models.board import Board
from dotenv import load_dotenv
import os

load_dotenv()

# App fixtures
@pytest.fixture(scope="session")
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI', 'sqlite:///:memory:'),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def push_app_context(app):
        yield



# Model fixtures
@pytest.fixture
def one_saved_board(app):
    board = Board(title="Pricilla's Board", owner="Pricilla")
    db.session.add(board)
    db.session.commit()
    return board

@pytest.fixture
def two_saved_boards(app):
    board1 = Board(title="Anaiah's Board", owner="Anaiah")
    board2 = Board(title="Nadia's Board", owner="Nadia")
    db.session.add_all([board1, board2])
    db.session.commit()
    return board1, board2

@pytest.fixture
def one_saved_card(app, one_saved_board):
    card = Card(message="YanYi is super smart.", board_id=one_saved_board.id)
    db.session.add(card)
    db.session.commit()
    return card

@pytest.fixture
def board_with_two_cards(app, one_saved_board):
    card1 = Card(message="This is the first test card.", board_id=one_saved_board.id)
    card2 = Card(message="This is the second test card.", board_id=one_saved_board.id)
    db.session.add_all([card1, card2])
    db.session.commit()
    return one_saved_board


