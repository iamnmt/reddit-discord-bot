import discord
from discord.ext import commands

import json

REDDIT_CATEGORY = ["best", "hot", "new"]
EMBED_COLOR = discord.Color.dark_red()


class Subscription(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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

        Reddit categories: best, hot, new

        Usage: !sub add [category] [subreddits...]
        Example: !sub add hot memes
    """,
    )
    async def add(self, ctx, category, *subreddits):
        if category not in REDDIT_CATEGORY:
            await ctx.send("Invalid category. Use `!help sub add` for more information")
            return

        for subreddit in subreddits:
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

    @add.error
    async def add_error(self, ctx, error):
        await ctx.invoke(self.bot.get_command("help"), "sub", "add")

    @sub.command(
        name="list",
        brief="List all subscribed subreddits",
        description="List all subscribed subreddits",
    )
    async def list(self, ctx):
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

        Reddit categories: best, hot, new

        Usage: !sub remove [category] [subreddits...]
        Example: !sub remove hot memes
    """,
    )
    async def remove(self, ctx, category, *subreddits):
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

    @remove.error
    async def remove_error(self, ctx, error):
        await ctx.invoke(self.bot.get_command("help"), "sub", "remove")


def setup(bot):
    bot.add_cog(Subscription(bot))
