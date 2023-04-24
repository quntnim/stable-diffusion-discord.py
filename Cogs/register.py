import discord
from discord import app_commands
from discord.ext import commands
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from var import *

class register(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="register")
    async def register(self, interaction: discord.Interaction) -> None:
        """디스코드 봇에 내 정보를 등록합니다."""
        json_data = {}
        with open(JSON_PATH, "r") as json_file:
            json_data = json.load(json_file)
        user_cnt = len(json_data['users'])

        is_exist = False
        for i in range(user_cnt):
            if interaction.user.id == json_data['users'][i]['userid']:
                is_exist = True
                break
        
        if is_exist:
            await interaction.response.send_message(f"{interaction.user.mention} 님은 이미 등록이 되어 있어요!",ephemeral=True)
        else:
            json_data['users'].append({
                    "userid": interaction.user.id,
                    "model": 'anything-v3-fp16-pruned',
                    "gen_count": 0
                })
            with open(JSON_PATH, 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            await interaction.response.send_message(f"{interaction.user.mention} 님을 등록했어요.",ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        register(bot),
        guilds=[discord.Object(id=GUILD_ID)]
    )