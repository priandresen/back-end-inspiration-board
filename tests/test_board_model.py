from app.models.board import Board
from app.db import db
import pytest

def test_board_creation():
    #Arrange
    title = "2026 Goals"
    owner = "Super Motivated Student"
    board = Board(title=title, owner=owner)
    db.session.add(board)
    db.session.commit()
    #Act
    board = Board.query.get(board.id)
    #Assert
    assert board.id is not None
    assert board.id == board,id
    assert board.title == title
    assert board.owner == owner

def test_board_missing_title_not_created():
    #Arrange
    board = Board(owner="Nesferatu")
    db.session.add(board)
    #Act
    db.session.commit()
    #Assert
    assert board.id is None, "Board without title should not be created"

def test_board_missing_owner_not_created():
    #Arrange
    board = Board(title="Spooky Board")
    db.session.add(board)
    #Act
    db.session.commit()
    #Assert
    assert board.id is None, "Board without owner should not be created"

def test_board_to_dict(one_saved_board):
    #Arrange
    board = one_saved_board
    #Act
    board_dict = board.to_dict()
    #Assert
    assert board_dict == {
        "id": board.id,
        "title": board.title,
        "owner": board.owner
    }

def test_board_from_dict():
    #Arrange
    board_dict = {
        "id": 1,
        "title": "Anaiah was here",
        "owner": "Anaiah"
    }
    #Act
    board = Board.from_dict(board_dict)
    #Assert
    assert isinstance(board, Board)
    assert board.title == "Anaiah was here"
    assert board.owner == "Anaiah"
    