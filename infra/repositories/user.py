from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from infra.database import Database
from models.constants import MODIFIED_AT_SORT_KEY
from models.enums import SortDirection
from models.exceptions import FilterDoesNotExistException, AlreadyExistsException, NotFoundException
from models.user import User
from bll.repositories import IUserRepository

class UserRepository(IUserRepository):
    def __init__(self, db: Database):
        self._session = next(db.session())

    def _get_user_or_none(self, id: UUID) -> Optional[User]:
        user = (
            self._session
                .query(User)
                .filter_by(id=id)
                .first()
        )

        return user
    
    def _get_user_by_email_or_none(self, email: str) -> Optional[User]:
        user = (
            self._session
                .query(User)
                .filter_by(email=email)
                .first()
        )
        return user
    
    def get_by_email(self, email:str) -> User:
        user: Optional[User] = self._get_user_by_email_or_none(email)
        if user is None:
            raise NotFoundException()
        
        return user

    def get_by_id(self, id: UUID) -> User:
        user: Optional[User] = self._get_user_or_none(id)
        if user is None:
            raise NotFoundException()
        
        return user

    def create(self, user: User) -> User:
        user_to_check: Optional[User] = self._get_user_by_email_or_none(user.email)
        if user_to_check:
            raise AlreadyExistsException()

        self._session.add(user)
        self._session.commit()

        return user
    
    def update(self, id: UUID, user: User) -> User:
        user_found: Optional[User] = self._get_user_or_none(id)
        if user_found is None:
            raise NotFoundException()
        
        obj_dict = user.__dict__
        user_dict = user_found.__dict__

        user_dict.update(obj_dict)
        user_found.__dict__ = user_dict

        self._session.commit()

        return user_found

    def delete(self, id: UUID) -> None:
        user: Optional[User] = self._get_user_or_none(id)
        if user is None:
            raise NotFoundException()
        
        self._session.delete(user)
        self._session.commit()

    def get(self, filter_by: Dict[str, Any], sort_by: str = MODIFIED_AT_SORT_KEY, sort_order: SortDirection = SortDirection.ASC, offset: int = 0, limit: int = 10) -> List[User]:
        try:
            sort_direction_func = desc if sort_order == SortDirection.DESC else asc

            users = (
                self._session
                    .query(User)
                    .filter_by(**filter_by)
                    .order_by(sort_direction_func(getattr(User, sort_by)))
                    .offset(offset)
                    .limit(limit)
                    .all()
            )

            return users
        
        except Exception as e:
            raise FilterDoesNotExistException()
