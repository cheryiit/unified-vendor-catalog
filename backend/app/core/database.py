from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.domain.entities.product import Product

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
POSTGRES_DATABASE_URL = settings.POSTGRES_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
pg_engine = create_engine(POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
PGSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)

Base = declarative_base()