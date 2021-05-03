from random import choice, randint

from discord.ext import tasks, commands
from sqlalchemy.orm import sessionmaker

from database import engine
from models import Coin


class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.worker.start()

    @tasks.loop(minutes=1)
    async def worker(self):
        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        import coins
        for coin in coins.__all__:
            coin = getattr(coins, coin)

            symbol = choice(['-', '+', '-', '+', '-'])
            new_price = randint(coin.MIN_RANGE, coin.MAX_RANGE)

            ctx = session.query(Coin).filter_by(
                name=coin.NAME
            ).first()

            if symbol == "+":
                ctx.price += new_price
            else:
                ctx.price -= new_price

            if ctx.price < coin.MIN_PRICE:
                ctx.price = coin.MIN_PRICE

            if coin.MAX_PRICE is not None:
                if ctx.price > coin.MAX_PRICE:
                    ctx.price = coin.MAX_PRICE

            print(f"{ctx.name} : {ctx.price} / {symbol}{new_price}")

        session.commit()
