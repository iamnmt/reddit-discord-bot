import discord
from discord.ext import commands

REDDIT_CATEGORY = ["best", "hot", "new"]


class Subscription(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.subs = dict()

    @commands.group(
        name="sub",
        brief="Subreddit commands",
        description="Subreddit commands",
        invoke_without_command=True,
    )
    async def sub(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command. Use `!sub help` for more information.")

    @sub.command(
        name="add",
        brief="Subscribe to a list of subreddits",
        description="""Subscribe to a list of subreddits

    Reddit categories: best, hot, new

    Example: !sub add hot memes
    """,
    )
    async def add(self, ctx, category, *subreddits):
        if category not in REDDIT_CATEGORY:
            await ctx.send("Invalid category. Use `!sub help` for more information")
            return

        for subreddit in subreddits:
            if subreddit not in self.subs:
                self.subs[subreddit] = [category]
            elif category not in self.subs[subreddit]:
                self.subs[subreddit].append(category)
            else:
                await ctx.send(
                    f"Already subscribed to {category} category of {subreddit}"
                )
                continue
            await ctx.send(f"Subscribed to {category} of {subreddit}")

    @sub.command(
        name="list",
        brief="List all subscribed subreddits",
        description="List all subscribed subreddits",
    )
    async def list(self, ctx):
        message = """```Subscribed subreddits:
        """
        for subreddit in self.subs.keys():
            message += (
                f"\n + {subreddit}: {', '.join(self.subs[subreddit])}"
            )
        message += "```"
        await ctx.send(message)

    @sub.command(
        name="remove",
        brief="Remove a list of subreddits",
        description="""Remove a list of subreddits

        Reddit categories: best, hot, new

        Example: !sub remove hot memes
    """,
    )
    async def remove(self, ctx, category, *subreddits):
        if category not in REDDIT_CATEGORY:
            await ctx.send("Invalid category. Use `!sub help` for more information.")
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


def setup(bot):
    bot.add_cog(Subscription(bot))
