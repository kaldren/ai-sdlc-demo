import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


def _build_database_url() -> str:
    explicit = os.environ.get("DATABASE_URL")
    if explicit:
        return explicit

    # Falls back to individual PG* vars so deployments can pass the password as its
    # own secret without ever concatenating it into a connection string in IaC.
    # URL.create percent-encodes each component, so special characters in the
    # password (e.g. "@", "%") can't corrupt the resulting URL.
    sslmode = os.environ.get("PGSSLMODE")
    url = URL.create(
        "postgresql+psycopg",
        username=os.environ.get("PGUSER", "taskuser"),
        password=os.environ.get("PGPASSWORD", "taskpass"),
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        database=os.environ.get("PGDATABASE", "tasktracker"),
        query={"sslmode": sslmode} if sslmode else {},
    )
    return url.render_as_string(hide_password=False)


DATABASE_URL = _build_database_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
