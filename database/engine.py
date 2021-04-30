
from sqlalchemy import create_engine

from database import URL


def get_engine():
    engine = create_engine(URL)
    return engine
