import discord
from discord.ext import commands

from utils.constants import EMBED_COLOR

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *input):
        is_valid_command = True
        emb = None

        if not input:
            # No input, list all commands

            description = f"{self.bot.description}\n\n"
            description += f"Use `{self.bot.command_prefix}help [command]` for more information about a command."

            emb = discord.Embed(
                title="Help Menu",
                color=EMBED_COLOR,
                description=description,
            )

            for cog in self.bot.cogs:
                if cog != "Help":
                    field_value = ""
                    for command in self.bot.cogs[cog].get_commands():
                        field_value += f"`{self.bot.command_prefix}{command.name}` - {command.brief}\n"
                    emb.add_field(name=cog, value=field_value)

            emb.add_field(
                name="About",
                value=f"GitHub repo: https://github.com/iamnmt/reddit-discord-bot",
            )
            emb.set_footer(text=f"ver 0.0.1")

        elif len(input) == 1:
            # One input, list all commands in that group

            # iterating through bot commands
            # because all commands are implemnted as commands.group,
            # we need to iterate through all of group's subcommands
            for group in self.bot.commands:
                if (
                    group.name.lower() == input[0].lower()
                    and group.name.lower() != "help"
                ):

                    description = f"{group.description}\n\n"
                    description += f"Use `{self.bot.command_prefix}help {group} [command]` for more information about a command. \n\n"

                    field_value = ""

                    for command in group.commands:
                        field_value += f"`{command.name}` - {command.brief}\n"

                    emb = discord.Embed(
                        title=f"Help for {self.bot.command_prefix}{group.name}",
                        description=description,
                        color=EMBED_COLOR,
                    )
                    emb.add_field(name="Commands", value=field_value)

                    break
            else:
                is_valid_command = False

        elif len(input) == 2:
            # Two inputs, info about a command in that group
            for command in self.bot.walk_commands():
                full_command = f"{command.parent} {command.name}".lower()
                if full_command == " ".join(input).lower():
                    emb = discord.Embed(
                        title=f"Help for {self.bot.command_prefix}{full_command}",
                        description=command.description,
                        color=EMBED_COLOR,
                    )
                    break
            else:
                is_valid_command = False

        else:
            is_valid_command = False

        if not is_valid_command:
            emb = discord.Embed(
                title="Invalid command",
                description=f"Use `{self.bot.command_prefix}help` to see all commands.",
                color=EMBED_COLOR,
            )

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))
