import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

description = """A bot that can subscribe to a list of subreddits and post them to a channel.
"""

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", description=description, intents=intents)

bot.run(os.getenv("DISCORD_TOKEN"))
