#!/usr/bin/env python3
from sys import exit, version_info as py_ver
from logging import INFO, getLogger, Formatter
from logging import StreamHandler, FileHandler

from discord import Status
from discord import version_info as dpy_ver
from discord.ext.commands import AutoShardedBot


bot = AutoShardedBot(
    command_prefix=";"
)

if __name__ == "__main__":
    logger = getLogger()
    logger.setLevel(INFO)
    fmt = Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
    s_handle, f_handle = StreamHandler(), FileHandler("bot.log")
    s_handle.setFormatter(fmt), f_handle.setFormatter(fmt)
    logger.addHandler(s_handle), logger.addHandler(f_handle)
    logger.info(
        "Starting discord bot / using"
        f" py({ py_ver.major}.{ py_ver.minor}.{ py_ver.micro}), "
        f"dpy({dpy_ver.major}.{dpy_ver.minor}.{dpy_ver.micro})"
    )

    try:
        with open("token.txt", mode="r") as tk:
            token = tk.readline()
    except FileNotFoundError:
        logger.critical("token undefined")
        exit(-1)

    import commands

    for command in commands.__all__:
        module = getattr(commands, command)
        bot.add_cog(getattr(module, "Cog")(bot))

    async def on_ready():
        await bot.change_presence(
            status=Status.dnd
        )

    async def on_command(ctx):
        logger.info(f"({ctx.author.id}){ctx.author}: {ctx.message.content}")


    async def on_command_error(ctx, error):
        if error.__class__.__name__ in ["CommandNotFound", "CheckFailure", "NotOwner"]:
            return

        if error.__class__.__name__ == "MissingRequiredArgument":
            return await ctx.reply("명령어에 필요한 옵션이 입력되지 않았습니다")

    bot.add_listener(on_ready, "on_ready")
    bot.add_listener(on_command, "on_command")
    bot.add_listener(on_command_error, "on_command_error")
    bot.run(token)
