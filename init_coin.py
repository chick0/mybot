
from sqlalchemy.orm import sessionmaker

from database import engine
from models import Coin
import coins

Session = sessionmaker(engine.get_engine())
session = Session()

for coin in coins.__all__:
    coin = getattr(coins, coin)

    c = session.query(Coin).filter_by(
        name=coin.NAME
    ).first()
    if c is not None:
        c.price = coin.MIN_PRICE
    else:
        c = Coin()
        c.name = coin.NAME
        c.price = coin.MIN_PRICE

        session.add(c)
        session.commit()
