import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.constants import COMMAND_PREFIX

load_dotenv()

description = """A bot that can subscribe to a list of subreddits and post them to a channel.
"""
help_command = commands.DefaultHelpCommand(no_category="Commands")
intents = discord.Intents.default()
bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    description=description,
    intents=intents,
    help_command=help_command,
)

bot.remove_command("help")

if __name__ == "__main__":
    bot.load_extension("cogs.subscription")
    print("Loaded cogs.subscription")
    bot.load_extension("cogs.action")
    print("Loaded cogs.action")
    bot.load_extension("cogs.help")
    print("Loaded cogs.help")

bot.run(os.getenv("DISCORD_TOKEN"))
