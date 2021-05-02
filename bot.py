#!/usr/bin/env python3
from sys import exit

from discord import Status
from discord.ext.commands import AutoShardedBot


bot = AutoShardedBot(
    command_prefix=";"
)


if __name__ == "__main__":
    try:
        with open("token.txt", mode="r") as tk:
            token = tk.readline()
    except FileNotFoundError:
        print("token undefined")
        exit(-1)

    import commands
    for command in commands.__all__:
        module = getattr(commands, command)
        bot.add_cog(getattr(module, "Cog")(bot))

    async def on_ready():
        await bot.change_presence(
            status=Status.dnd
        )

    bot.add_listener(on_ready, "on_ready")
    bot.run(token)
    del token
