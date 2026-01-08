from app.models.board import Board
# from app.models.card import Card
import pytest

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
    