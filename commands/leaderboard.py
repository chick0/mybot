
from discord import Embed
from discord.ext import commands
from sqlalchemy.orm import sessionmaker

from database import engine
from models import Point


class Cog(commands.Cog, name="리더보드"):
    @commands.command(help="순위 확인")
    async def leaderboard(self, ctx: commands.context):
        embed = Embed(
            title="리더보드",
            color=0xF7F7F7
        )

        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        for i, x in enumerate(session.query(Point).order_by(
            Point.point.desc()
        ).limit(25).all()):
            embed.add_field(
                name=f"{i + 1} 위",
                value=f"{x.point} P",
                inline=False
            )

        await ctx.send(
            embed=embed
        )
