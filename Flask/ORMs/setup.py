from ORMs.db import engine
from ORMs.models import Base

Base.metadata.create_all(engine)