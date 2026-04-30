from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORMs.models import Base

DATABASE_URL = "sqlite:///car_rental.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
