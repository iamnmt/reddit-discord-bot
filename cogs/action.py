import os
import json
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext import tasks

from reddit.auth.headers import make_headers
from reddit.action.fetch import fetch_img

load_dotenv()

SUPPORTED_TASKS = ["image"]
EMBED_COLOR = discord.Color.dark_red()


class Action(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printers = {
            "image": None,
        }

    @commands.group(
        name="fetch",
        brief="Fetching commands",
        description="Fetching commands",
        invoke_without_command=True,
    )
    async def fetch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command("help"), "fetch")

    @fetch.command(
        name="image",
        brief="Fetch images from subscribed subreddits",
        description="Fetch images from subscribed subreddits",
    )
    async def fetch_image(self, ctx):
        data = None
        with open("subscription.json", "r") as f:
            data = json.load(f)
        if data:
            subs = data["subs"]
            headers = None
            if os.environ.get("IS_DEV", False):
                print("Using saved headers")
                with open("headers.json", "r") as f:
                    headers = json.load(f)
            else:
                headers = make_headers(
                    os.environ["REDDIT_CLIENT_ID"],
                    os.environ["REDDIT_PRIVATE_KEY"],
                    os.environ["REDDIT_ACCOUNT_USERNAME"],
                    os.environ["REDDIT_ACCOUNT_PASSWORD"],
                )
            result_dict = fetch_img(headers, subs)
            for sub in result_dict.keys():
                for category in result_dict[sub].keys():
                    for post in result_dict[sub][category]:
                        title, url = post["title"], post["url"]
                        embed = discord.Embed(
                            title=title,
                            description=f"{sub}/{category}",
                            color=EMBED_COLOR,
                        )
                        embed.set_image(url=url)
                        await ctx.send(embed=embed)

            headers = None

    @commands.group(
        name="schedule",
        brief="Scheduling commands",
        description="Scheduling commands",
        invoke_without_command=True,
    )
    async def schedule(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command("help"), "schedule")

    @schedule.command(
        name="image",
        brief="Schedule image fetching task",
        description="""
        Schedule image fetching task

        Usage: !schedule image [interval (in hours)]
        Example: !schedule image 1
    """,
    )
    async def schedule_image(self, ctx, interval: int):
        if interval <= 0:
            await ctx.send("Interval must be greater than 0")
            return

        @tasks.loop(hours=interval)
        async def fetch_image():
            await self.fetch_image(ctx)

        self.printers["image"] = {
            "interval": interval,
            "task": fetch_image,
        }
        self.printers["image"]["task"].start()
        await ctx.send("Scheduled image fetching")

    @schedule.command(
        name="clear",
        brief="Clear scheduled task",
        description="""
        Clear scheduled task

        Usage: !schedule clear [task (image)]
        Example: !schedule clear image
    """,
    )
    async def schedule_clear(self, ctx, *tasks):
        if len(tasks) == 0:
            for task in SUPPORTED_TASKS:
                if self.printers[task]:
                    self.printers[task]["task"].cancel()
                    self.printers[task] = None
            await ctx.send("Cleared all scheduled tasks")
            return
        for task in tasks:
            if task not in SUPPORTED_TASKS:
                await ctx.send(
                    f"Invalid task ({task}). Use `!help schedule clear` for more information."
                )
                return
            if self.printers[task]:
                self.printers[task]["task"].cancel()
                self.printers[task] = None
                await ctx.send(f"Cleared scheduled {task} task")

    @schedule.command(
        name="list", brief="List scheduled tasks", description="List scheduled tasks"
    )
    async def schedule_list(self, ctx):
        embed = discord.Embed(
            title="Scheduled tasks",
            color=EMBED_COLOR,
        )
        for task in SUPPORTED_TASKS:
            if self.printers[task]:
                embed.add_field(
                    name=f"{task}",
                    value=f"{self.printers[task]['interval']} hours",
                )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Action(bot))
