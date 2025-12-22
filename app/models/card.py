from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .card import Card

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int]

    # def to_dict(self):

    #     goal_dict = {
    #         "id": self.id,
    #         "title": self.title
    #     }
    #     # if self.tasks:
    #     #     goal_dict["tasks"] = [task.to_dict() for task in self.tasks]

    #     return goal_dict
    
    # def to_dict_with_task(self):

    #     goal_dict_with_task = {
    #         "id" : self.id,
    #         "task_ids" : [task.id for task in self.tasks]
    #     }

    #     return goal_dict_with_task

    # @classmethod
    # def from_dict(cls, data):
    #     return cls(title=data["title"])
    