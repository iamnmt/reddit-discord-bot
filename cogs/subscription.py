import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncpraw

import json

from utils.constants import REDDIT_CATEGORY, EMBED_COLOR

load_dotenv()

class Subscription(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_PRIVATE_KEY"],
            user_agent="reddit-discord-bot v0.0.1",
        )

        with open("subscription.json", "r") as f:
            self.data = json.load(f)
        self.subs = self.data["subs"]

    @commands.group(
        name="sub",
        brief="Subreddit commands",
        description="Subreddit commands",
        invoke_without_command=True,
    )
    async def sub(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command("help"), "sub")

    @sub.command(
        name="add",
        brief="Subscribe to a list of subreddits",
        description="""
        Subscribe to a list of subreddits

        Reddit categories: top, hot, new

        Usage: !sub add [category] [subreddits...]
        Example: !sub add hot memes
    """,
    )
    async def sub_add(self, ctx, category, *subreddits):
        if category not in REDDIT_CATEGORY:
            await ctx.send("Invalid category. Use `!help sub add` for more information")
            return

        for subreddit in subreddits:
            # Check if subreddit exists
            try:
                # Have to loop over the list of subreddits because from the docs:
                # """
                # The act of calling a method that returns a ListingGenerator
                # does not result in any network requests until you begin to
                # iterate through the ListingGenerator.
                # """
                async for _ in self.reddit.subreddits.search_by_name(
                    subreddit, exact=True
                ):
                    pass
            except:
                await ctx.send(f"Subreddit {subreddit} not found")
                continue

            if subreddit not in self.subs:
                self.subs[subreddit] = [category]
            elif category not in self.subs[subreddit]:
                self.subs[subreddit].append(category)
            else:
                await ctx.send(f"Already subscribed to {category} of {subreddit}")
                continue
            await ctx.send(f"Subscribed to {category} of {subreddit}")

        with open("subscription.json", "w") as f:
            json.dump(self.data, f, indent=4)

    @sub_add.error
    async def sub_add_error(self, ctx, error):
        await ctx.invoke(self.bot.get_command("help"), "sub", "add")

    @sub.command(
        name="list",
        brief="List all subscribed subreddits",
        description="List all subscribed subreddits",
    )
    async def sub_list(self, ctx):
        embed = discord.Embed(
            title="Subscribed subreddits",
            description="\n".join(
                [
                    f"{subreddit} - {', '.join(categories)}"
                    for subreddit, categories in self.subs.items()
                ]
            ),
            color=EMBED_COLOR,
        )
        await ctx.send(embed=embed)

    @sub.command(
        name="remove",
        brief="Remove a list of subreddits",
        description="""
        Remove a list of subreddits

        Reddit categories: top, hot, new

        Usage: !sub remove [category] [subreddits...]
        Example: !sub remove hot memes
    """,
    )
    async def sub_remove(self, ctx, category, *subreddits):
        if category not in REDDIT_CATEGORY:
            await ctx.send(
                "Invalid category. Use `!help sub remove` for more information."
            )
            return
        for subreddit in subreddits:
            if subreddit not in self.subs:
                await ctx.send(f"{subreddit} is not subscribed")
                continue
            elif category in self.subs[subreddit]:
                self.subs[subreddit].remove(category)
                if len(self.subs[subreddit]) == 0:
                    del self.subs[subreddit]
                await ctx.send(f"Removed {category} from {subreddit}")

        with open("subscription.json", "w") as f:
            json.dump(self.data, f, indent=4)

    @sub_remove.error
    async def sub_remove_error(self, ctx, error):
        await ctx.invoke(self.bot.get_command("help"), "sub", "remove")


def setup(bot):
    bot.add_cog(Subscription(bot))
