
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
    async def buy(self, ctx: commands.context, code: str, count: int = 1):
        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        if count <= 0:
            count = 1

        cn = session.query(Coin).filter_by(
            name=code
        ).first()
        if cn is None:
            await ctx.reply(
                "등록된 코인이 아닙니다."
            )
        else:
            wl = session.query(Wallet).filter_by(
                name=code,
                owner=ctx.author.id
            ).first()

            if wl is None:
                wl = Wallet()
                wl.name = code
                wl.owner = ctx.author.id
                wl.count = 0

                session.add(wl)

            wl_point = session.query(Point).filter_by(
                owner=ctx.author.id
            ).first()

            if wl_point.point - (cn.price * count) >= 0:
                wl.count += count
                wl_point.point -= cn.price * count
                session.commit()

                await ctx.reply(
                    "구매 성공\n"
                    "```\n"
                    "-----------------------------------\n"
                    f"- 거래한 코인: {count} 개\n"
                    f"- 코인 거래 가격: {cn.price} P\n"
                    f"- 거래 후 보유중인 코인: {wl.count} 개\n"
                    "-----------------------------------\n"
                    f"- 변동 포인트 : -{cn.price * count} P\n"
                    f"- 거래 후 남은 포인트: {wl_point.point} P\n"
                    "-----------------------------------\n"
                    "```"
                )
            else:
                await ctx.reply(
                    "구매 실패"
                    "```\n"
                    "-----------------------------------\n"
                    f"- 거래한 코인: 0 개\n"
                    f"- 코인 거래 가격: {cn.price} P\n"
                    f"- 거래 후 보유중인 코인: {wl.count} 개\n"
                    "-----------------------------------\n"
                    f"- 변동 포인트 : -0 P\n"
                    f"- 거래 후 남은 포인트: {wl_point.point} P\n"
                    "-----------------------------------\n"
                    "```"
                )
