from sqlalchemy import String, CheckConstraint, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped

from entities.base import Base

class UserEntity(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(300), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    todos = relationship("TodoItemEntity", back_populates="owner")

    __table_args__ = (
        CheckConstraint(
            r"email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'", 
            name='email_format_check'
        ),
        CheckConstraint(
            "LENGTH(name) >= 1", 
            name="name_min_length_check"
        ),
        CheckConstraint(
            r"name ~* '^[A-Za-z]+$'", 
            name="name_alphabetic_check"
        ),
    )