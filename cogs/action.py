import os
import json
from dotenv import load_dotenv
import discord
from discord.ext import commands

from reddit.auth.headers import make_headers
from reddit.action.fetch import fetch_img

load_dotenv()


class Action(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="fetch",
        brief="Fetching commands",
        description="Subreddit commands",
        invoke_without_command=True,
    )
    async def fetch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command. Use `!fetch help` for more information.")

    @fetch.command(
        name="image",
        brief="Fetch images from subscribed subreddits",
        description="Fetch images from subscribed subreddits",
    )
    async def image(self, ctx):
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
                            title=title, description=f"{sub}/{category}"
                        )
                        embed.set_image(url=url)
                        await ctx.send(embed=embed)

            headers = None


def setup(bot):
    bot.add_cog(Action(bot))
