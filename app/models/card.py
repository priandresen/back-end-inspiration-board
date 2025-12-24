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
        card = cls(
                message=data["message"],
                board_id=data["board_id"]
        )
        return card  

    