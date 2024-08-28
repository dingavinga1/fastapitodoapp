from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from sqlalchemy import UUID as UUIDType
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

class BaseEntity(object):
    id: Mapped[UUID] = mapped_column(UUIDType, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc))
    modified_at: Mapped[datetime] = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))

Base = declarative_base(cls=BaseEntity)