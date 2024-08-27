from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from bll.repositories.ienvironment import IEnvironmentVariables

class Database:
    def __init__(self, env: IEnvironmentVariables) -> None:
        DATABASE_URL = f"postgresql+psycopg2://{env.get_var("DB_USER")}:{env.get_var("DB_PASS")}@{env.get_var("DB_HOST")}:{env.get_var("DB_PORT")}/{env.get_var("DB_NAME")}"

        self._engine = create_engine(
            DATABASE_URL,
            echo = env.DEBUG_MODE
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