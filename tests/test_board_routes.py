import pytest
from app.models.board import Board
from app.models.card import Card


def test_get_all_boards(client, two_saved_boards):
    response = client.get("/boards")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert all("id" in board for board in data)
    assert all("title" in board for board in data)
    assert all("owner" in board for board in data)


def test_get_one_board(client, one_saved_board):
    board_id = one_saved_board
    response = client.get(f"/boards/{board_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == board_id
    assert data["title"] == "Pricilla's Board"
    assert data["owner"] == "Pricilla"


def test_get_one_board_not_found(client):
    response = client.get("/boards/9999")
    assert response.status_code == 404


def test_get_cards_for_board(client, board_with_two_cards):
    board_id = board_with_two_cards
    response = client.get(f"/boards/{board_id}/cards")
    data = response.get_json()

    assert response.status_code == 200
    assert "cards" in data
    assert len(data["cards"]) == 2
    assert all(card["board_id"] == board_id for card in data["cards"])



def test_create_board(client):
    request_body = {"title": "Cinderella Vibes", "owner": "YanYi"}
    response = client.post("/boards", json=request_body)
    data = response.get_json()

    assert response.status_code == 201
    assert data["title"] == "Cinderella Vibes"
    assert data["owner"] == "YanYi"
    assert "id" in data



def test_create_card_for_board(client, one_saved_board):
    board_id = one_saved_board
    request_body = {"message": "Test card"}
    response = client.post(f"/boards/{board_id}/cards", json=request_body)
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Test card"
    assert data["board_id"] == board_id
    assert data["likes_count"] == 0


def test_create_card_missing_message(client, one_saved_board):
    board_id = one_saved_board
    request_body = {}

    response = client.post(f"/boards/{board_id}/cards", json=request_body)
    data = response.get_json()

    assert response.status_code == 400
    assert "Request body must include 'message'." in data.values()




def test_delete_board(client, board_with_two_cards):
    board_id = board_with_two_cards

    response = client.delete(f"/boards/{board_id}")

    assert response.status_code == 204
    assert Board.query.get(board_id) is None
    assert Card.query.filter_by(board_id=board_id).count() == 0




def test_delete_all_cards_in_board(client, board_with_two_cards):
    board_id = board_with_two_cards

    response = client.delete(f"/boards/{board_id}/cards")

    assert response.status_code == 204

    cards_in_db = Card.query.filter_by(board_id=board_id).all()
    assert len(cards_in_db) == 0
