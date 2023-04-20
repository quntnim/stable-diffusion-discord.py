import discord
from discord import app_commands
from discord.ext import commands
from var import *

class ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction) -> None:
        """퐁!
        """
        await interaction.response.send_message(f"pong! {interaction.id}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        ping(bot),
        guilds=[discord.Object(id=guildid)]
    )