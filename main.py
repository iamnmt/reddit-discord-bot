import discord
from discord.ext import commands

import os
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

subscribed_subreddits = dict()

REDDIT_CATEGORY = ["best", "hot", "new"]

@bot.group(
    name="sub",
    brief="Subscription commands",
    description="Subscription commands",
    invoke_without_command=True,
)
async def sub(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Invalid command. Use `!sub help` for more information.")


@sub.command(
    name="add", brief="Subscribe to a list of subreddits", description="""Subscribe to a list of subreddits

    Reddit categories: best, hot, new

    Example: !sub add hot memes
    """
)
async def add(ctx, category, *subreddits):
    if category not in REDDIT_CATEGORY:
        await ctx.send("Invalid category. Use `!sub help` for more information")
        return

    for subreddit in subreddits:
        if subreddit not in subscribed_subreddits:
            subscribed_subreddits[subreddit] = [category]
        elif category not in subscribed_subreddits[subreddit]:
            subscribed_subreddits[subreddit].append(category)
        else:
            await ctx.send(f"Already subscribed to {category} category of {subreddit}")
            return 
        await ctx.send(f"Subscribed to {category} of {subreddit}")

@sub.command(
    name="list", brief="List all subscribed subreddits", description="List all subscribed subreddits"
)
async def list(ctx):
    message = """```Subscribed subreddits:
    """
    for subreddit in subscribed_subreddits.keys():
        message += f"\n + {subreddit}: {', '.join(subscribed_subreddits[subreddit])}"
    message += "```"
    await ctx.send(message)

@sub.command(name="remove", brief="Remove a list of subreddits", description="""Remove a list of subreddits

    Reddit categories: best, hot, new

    Example: !sub remove hot memes
""")
async def remove(ctx, category, *subreddits):
    if category not in REDDIT_CATEGORY:
        await ctx.send("Invalid category. Use `!sub help` for more information.")
        return
    for subreddit in subreddits:
        if subreddit not in subscribed_subreddits:
            await ctx.send(f"{subreddit} is not subscribed")
            return
        elif category in subscribed_subreddits[subreddit]:
            subscribed_subreddits[subreddit].remove(category)
            if len(subscribed_subreddits[subreddit]) == 0:
                del subscribed_subreddits[subreddit]
            await ctx.send(f"Removed {category} from {subreddit}")

bot.run(os.getenv("DISCORD_TOKEN"))
