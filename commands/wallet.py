
from discord import Embed
from discord.ext import commands
from sqlalchemy.orm import sessionmaker

from database import engine
from models import Wallet, Point


class Cog(commands.Cog, name="지갑"):
    @commands.command(help="지갑 확인")
    async def wallet(self, ctx: commands.context):
        embed = Embed(
            title="지갑",
            color=0xF7F7F7
        )

        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        point = session.query(Point).filter_by(
            owner=str(ctx.author.id)
        ).first()

        point = point.point if point is not None else -1

        embed.description = f"{ctx.author.name}님의 포인트 : {point} P"

        import coins
        for cn in session.query(Wallet).filter_by(
            owner=str(ctx.author.id)
        ).all():
            embed.add_field(
                name="{name} 코인 ({code})".format(
                    name=getattr(getattr(coins, cn.name), "DISPLAY_NAME"),
                    code=getattr(getattr(coins, cn.name), "NAME")
                ),
                value=f"{cn.count} 개"
            )

        await ctx.send(
            embed=embed
        )

    @commands.command(help="지갑 만들기")
    async def create(self, ctx: commands.context):
        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        point = session.query(Point).filter_by(
                owner=str(ctx.author.id)
        ).first()
        if point is not None:
            await ctx.reply(
                "**경고** 당신은 이미 포인트 지갑을 가지고 있습니다."
            )
        else:
            point = Point()
            point.owner = str(ctx.author.id)
            point.point = 0

            session.add(point)
            session.commit()

            await ctx.reply(
                "포인트 지갑 생성 완료"
            )
