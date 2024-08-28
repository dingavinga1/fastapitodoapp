from unittest.mock import Base
from uuid import UUID
from sqlalchemy import String, CheckConstraint, Text, ForeignKey
from sqlalchemy import UUID as UUIDType
from sqlalchemy.orm import relationship, Mapped, mapped_column

from entities.base import Base

class TodoItemEntity(Base):
    __tablename__ = "todos"

    name: Mapped[str] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[UUID] = mapped_column(UUIDType, ForeignKey("users.id"))

    owner = relationship("UserEntity", back_populates="todos")

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) >= 1", 
            name="name_min_length_check"
        ),
    )