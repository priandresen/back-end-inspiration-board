from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .board import Board

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    likes_count: Mapped[int] = mapped_column(nullable=False, default=0)
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"), nullable=False) 
    board: Mapped["Board"] = relationship(back_populates="cards")


    def to_dict(self) -> dict:
        card_as_dict = {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id,
        }
        return card_as_dict


    @classmethod
    def from_dict(cls, data: dict):
        if "message" not in data:
            raise KeyError("message")

        message = data["message"]
        if message is None or not isinstance(message, str):
            raise ValueError("message must be a string")

        message = message.strip()
        if message == "":
            raise ValueError("message cannot be blank")
        if len(message) > 40:
            raise ValueError("message must be 40 characters or fewer")

        if "board_id" not in data:
            raise KeyError("board_id")
        
        try:
            board_id = int(data["board_id"])
        except (TypeError, ValueError):
            raise ValueError("board_id must be an integer")
        
        card = cls(
                message=message,
                board_id=board_id
        )
        return card