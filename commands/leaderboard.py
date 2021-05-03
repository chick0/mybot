
from discord import Embed
from discord.ext import commands
from sqlalchemy.orm import sessionmaker

from database import engine
from models import Point


class Cog(commands.Cog, name="리더보드"):
    @commands.command(help="순위 확인")
    @commands.cooldown(10, 30, commands.BucketType.guild)
    async def leaderboard(self, ctx: commands.context):
        embed = Embed(
            title="리더보드",
            color=0x99FF99
        )

        session_ = sessionmaker(bind=engine.get_engine())
        session = session_()

        for i, x in enumerate(session.query(Point).order_by(
            Point.point
        ).limit(25).all()):
            embed.add_field(
                name=f"{i + 1} 위",
                value=f"{x.point} P",
                inline=False
            )

        await ctx.send(
            embed=embed
        )
