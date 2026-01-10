# init_db.py -> run this once before actual app

from db import engine
from models import Base

Base.metadata.create_all(engine)
