import os
from glob import glob

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

description = """A bot that can subscribe to a list of subreddits and post them to a channel.
"""
help_command = commands.DefaultHelpCommand(no_category="Commands")
intents = discord.Intents.default()
bot = commands.Bot(
    command_prefix="!",
    description=description,
    intents=intents,
    help_command=help_command,
)

bot.remove_command("help")


@bot.command(name="test")
async def test(ctx, *file_names):
    file_paths = None
    if len(file_names) == 0:
        file_paths = glob(os.path.join("test", "*.txt"))
    else:
        file_paths = [os.path.join("test", f"{name}.txt") for name in file_names]
    for path in file_paths:
        print(f"Running commands from {path}")
        with open(path, "r") as f:
            while True:
                line = f.readline().split()
                if not line:
                    break
                command = bot.get_command(line[0])
                args_index = 1
                if isinstance(command, commands.Group):
                    command = command.get_command(line[1])
                    args_index = 2
                args = [
                    int(arg) if arg.isnumeric() else arg for arg in line[args_index:]
                ]
                await ctx.send(f"{bot.command_prefix}{' '.join(line)}")
                await ctx.invoke(command, *args)


if __name__ == "__main__":
    bot.load_extension("cogs.subscription")
    print("Loaded cogs.subscription")
    bot.load_extension("cogs.action")
    print("Loaded cogs.action")
    bot.load_extension("cogs.help")
    print("Loaded cogs.help")

bot.run(os.getenv("DISCORD_TOKEN"))
