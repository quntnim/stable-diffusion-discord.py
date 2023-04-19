import discord
from discord import app_commands
from discord.ext import commands
import json
import requests
import io
import base64
from var import *

class memory(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="memory")
    async def memory(self, interaction: discord.Interaction) -> None:
        """현재 서버 컴퓨터의 RAM과 VRAM 사용량을 알려 줍니다."""
        response = requests.get(url=f'{url}/sdapi/v1/memory')
        data = json.loads(response.text)
        await interaction.response.send_message(
            f"사용 가능 RAM: **{data['ram']['free']/1e+9:.1f}GB**\n전체 메모리 **{data['ram']['total']/1e+9:.1f}GB** 중 **{data['ram']['used']/1e+9:.1f}GB** 사용 중\n\n사용 가능 VRAM : **{data['cuda']['system']['free']/1e+9:.1f}GB**\n전체 메모리 **{data['cuda']['system']['total']/1e+9:.1f}GB** 중 **{data['cuda']['system']['used']/1e+9:.1f}GB** 사용 중")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        memory(bot),
        guilds=[discord.Object(id=guildid)]
    )