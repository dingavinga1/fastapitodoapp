from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

class Database:
    def __init__(self, host, name, port, user, password, debug_mode) -> None:
        DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

        self._engine = create_engine(
            DATABASE_URL,
            echo = debug_mode
        )
        
        self._session = scoped_session(sessionmaker(
            autocommit = False,
            autoflush = False,
            bind = self._engine
        ))
        
    def session(self) -> Generator[Session, None, None]:
        session: Session = self._session()
        try:
            yield session
        except:
            session.rollback()
        finally:
            session.close()