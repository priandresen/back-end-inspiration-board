from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .card import Card

class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    owner: Mapped[str] = mapped_column(String(100))
    cards: Mapped[list["Card"]] = relationship(back_populates="board", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
                title=data["title"],
                owner=data["owner"]
            )