
from discord import Embed
from discord.ext import commands


class Cog(commands.Cog, name="코인 정보"):
    @commands.command(help="코인 정보 확인")
    @commands.cooldown(10, 30, commands.BucketType.guild)
    async def stat(self, ctx: commands.context, code: str = None):
        if code is None:
            return await ctx.reply(
                "정보 조회할 코인의 거래코드를 명령어와 함께 입력해야 합니다"
            )

        import coins
        if code not in coins.__all__:
            return await ctx.reply(
                "등록된 코인이 아닙니다."
            )

        coin = getattr(coins, code)
        embed = Embed(
            title=f"{coin.DISPLAY_NAME} 코인",
            color=0xF7F7F7
        )
        embed.set_footer(
            text="주의) 코인의 정보는 언제든지 변경될 수 있습니다."
        )

        embed.add_field(
            name="변동 범위",
            value=f"{coin.MIN_RANGE} ~ {coin.MAX_RANGE}",
            inline=False
        )
        embed.add_field(
            name="최저 가격",
            value=f"{coin.MIN_PRICE} P",
            inline=False
        )
        embed.add_field(
            name="최고 가격",
            value=f"{coin.MAX_PRICE} P" if coin.MAX_PRICE is not None else "제한없음",
            inline=False
        )

        await ctx.send(
            embed=embed
        )
