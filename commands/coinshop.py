
from discord import Embed
from discord.ext import commands
from sqlalchemy.orm import sessionmaker

from database import engine
from models import Coin, Wallet, Point


class Cog(commands.Cog, name="코인상점"):
    @commands.command(help="시세 확인")
    @commands.cooldown(10, 30, commands.BucketType.guild)
    async def shop(self, ctx: commands.context):
        embed = Embed(
            title="코인상점",
            color=0x99FF99
        )
        embed.set_footer(
            text="괄호안에 텍스트는 거래코드 입니다 (거래코드는 구매&판매 할 때 사용됨)"
        )

        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        import coins
        for coin in coins.__all__:
            cn = session.query(Coin).filter_by(
                name=getattr(getattr(coins, coin), "NAME")
            ).first()

            embed.add_field(
                name="{name} 코인 ({code})".format(
                    name=getattr(getattr(coins, coin), "DISPLAY_NAME"),
                    code=getattr(getattr(coins, coin), "NAME")
                ),
                value=f"{cn.price} P"
            )

        await ctx.send(
            embed=embed
        )

    @commands.command(help="코인 구매")
    @commands.cooldown(10, 30, commands.BucketType.guild)
    async def buy(self, ctx: commands.context):
        embed = Embed(
            title="코인상점",
            color=0x99FF99
        )

        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        import coins
        for coin in coins.__all__:
            cn = session.query(Coin).filter_by(
                name=getattr(getattr(coins, coin), "NAME")
            ).first()

            embed.add_field(
                name=getattr(getattr(coins, coin), "DISPLAY_NAME") + " 코인",
                value=f"{cn.price} P"
            )

        await ctx.send(
            embed=embed
        )
