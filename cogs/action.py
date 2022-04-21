import json
import os

import asyncpraw
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from utils.constants import EMBED_COLOR, PRAW_SUBMISSION_LIMIT, SUPPORTED_TASKS

load_dotenv()


class Action(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_PRIVATE_KEY"],
            user_agent="reddit-discord-bot v0.0.1",
        )
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
            sub_to_category = data["subs"]
            for sub in sub_to_category.keys():
                print(f"Fetching images from {sub}")
                for category in sub_to_category[sub]:
                    subreddit = await self.reddit.subreddit(sub)
                    submissions_list = None
                    if category == "top":
                        submissions_list = subreddit.top(limit=PRAW_SUBMISSION_LIMIT)
                    elif category == "hot":
                        submissions_list = subreddit.hot(limit=PRAW_SUBMISSION_LIMIT)
                    elif category == "new":
                        submissions_list = subreddit.new(limit=PRAW_SUBMISSION_LIMIT)
                    async for submission in submissions_list:
                        if submission.is_self:
                            continue
                        url = submission.url
                        if url.endswith(".jpg") or url.endswith(".png"):
                            title = submission.title
                            permalink = submission.permalink
                            embed = discord.Embed(
                                title=title,
                                description=f"{sub}/{category}",
                                url=f"https://reddit.com{permalink}",
                                color=EMBED_COLOR,
                            )
                            embed.set_image(url=url)
                            await ctx.send(embed=embed)
                            break

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

    @schedule_image.error
    async def schedule_image_error(self, ctx, error):
        await ctx.invoke(self.bot.get_command("help"), "schedule", "image")

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
