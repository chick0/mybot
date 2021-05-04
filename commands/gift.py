from random import randint
from datetime import datetime, timedelta

from discord.ext import commands
from sqlalchemy.orm import sessionmaker

from database import engine
from models import Point, Gift


async def gift(session, ctx: commands.context, a: int, b: int):
    point = session.query(Point).filter_by(
        owner=ctx.author.id
    ).first()
    if point is None:
        point = Point()
        point.owner = ctx.author.id
        point.point = 0
        session.add(point)

    gift_point = randint(a, b)
    point.point += gift_point
    session.commit()

    await ctx.reply(
        f"선물 상자에서 {gift_point}P 를 받았습니다!"
    )


class Cog(commands.Cog, name="선물 상자"):
    @commands.command(help="24시간 마다")
    async def daily(self, ctx: commands.context):
        gift_code = "24h"

        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        gift_stat = session.query(Gift).filter_by(
            owner=ctx.author.id,
            type=gift_code
        ).first()
        if gift_stat is None:
            gift_stat = Gift()
            gift_stat.owner = ctx.author.id
            gift_stat.type = gift_code
            gift_stat.date = datetime.now() + timedelta(hours=24)

            session.add(gift_stat)
            session.commit()
            await gift(
                session, ctx, a=300, b=500
            )
        else:
            if gift_stat.date <= datetime.now():
                gift_stat.date = datetime.now() + timedelta(hours=24)
                session.commit()
                await gift(
                    session, ctx, a=300, b=500
                )
            else:
                await ctx.reply(
                    "아직 선물 상자가 도착하지 않았습니다"
                )



