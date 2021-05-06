from datetime import datetime
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
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        import coins
        for coin in coins.__all__:
            coin = getattr(coins, coin)

            ctx = session.query(Coin).filter_by(
                name=coin.NAME
            ).first()

            symbol = choice(['-', '+', '-', '+', '-'])
            old_price = ctx.price
            new_price = randint(coin.MIN_RANGE, coin.MAX_RANGE)

            if symbol == "+":
                ctx.price += new_price
            else:
                ctx.price -= new_price

            if ctx.price < coin.MIN_PRICE:
                ctx.price = coin.MIN_PRICE

            if coin.MAX_PRICE is not None:
                if ctx.price > coin.MAX_PRICE:
                    ctx.price = coin.MAX_PRICE

            with open("coin_update.csv", mode="a", encoding="utf-8") as fp:
                fp.write(f"{date}, {ctx.name}, {symbol}{new_price}, {old_price}, {ctx.price}\n")

        session.commit()
