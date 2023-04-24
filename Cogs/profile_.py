import discord
from discord import app_commands
from discord.ext import commands
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from var import *

class profile_(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="profile")
    async def profile_(self, interaction: discord.Interaction) -> None:
        """유저의 프로필을 보여 줍니다."""
        json_data = {}
        with open(JSON_PATH, "r") as json_file:
            json_data = json.load(json_file)
        user_cnt = len(json_data['users'])

        is_exist = False
        for i in range(user_cnt):
            if interaction.user.id == json_data['users'][i]['userid']:
                is_exist = True
                data = json_data['users'][i]
                break
        
        if is_exist:
            embed=discord.Embed(title="유저 정보",description=interaction.user.mention, color=0xF3A4B5)
            embed.set_thumbnail(url=interaction.user.avatar.url)
            embed.add_field(name="모델", value=data['model'], inline=True)
            embed.add_field(name="VAE", value=f"kl-f8-anime2.ckpt", inline=True)
            embed.add_field(name="생성 횟수", value=data['gen_count'], inline=True)
            embed.set_footer(text="@bocchi#9621")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"<@{interaction.user.id}>님은 아직 등록이 되어 있지 않아요!\n **/register** 으로 등록해주세요.",ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        profile_(bot),
        guilds=[discord.Object(id=GUILD_ID)]
    )