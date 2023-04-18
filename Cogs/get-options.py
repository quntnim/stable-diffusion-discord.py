import discord
from discord import app_commands
from discord.ext import commands
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from var import *

class get_options(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="get-options")
    async def get_options(self, interaction: discord.Interaction) -> None:
        """현재 설정되있는 모델과 vae를 알려 줍니다."""
        response = requests.get(url=f'{url}/sdapi/v1/options',)
        data = json.loads(response.text)
        await interaction.response.send_message(f"{data['sd_model_checkpoint']},{data['sd_vae']}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        get_options(bot),
        guilds=[discord.Object(id=guildid)]
    )