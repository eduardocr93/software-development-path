from sqlalchemy import create_engine
from ORMs.models import Base

engine = create_engine("sqlite:///car_rental.db")
Base.metadata.create_all(engine)
