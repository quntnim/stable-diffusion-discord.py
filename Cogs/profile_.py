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
    async def profile_(self, interaction: discord.Interaction, user: discord.user.User = None) -> None:
        """유저의 프로필을 보여 줍니다.
        
        인자
        ----------
        user: discord.user.User
            프로필을 확인할 유저입니다. 기본값 - None
        """
        json_data = {}
        with open(JSON_PATH, "r") as json_file:
            json_data = json.load(json_file)
        user_cnt = len(json_data['users'])

        find = interaction.user if user == None else user
        is_exist = False
        for i in range(user_cnt):
            if find.id == json_data['users'][i]['userid']:
                is_exist = True
                data = json_data['users'][i]
                break
        
        if is_exist:
            gen_count = data['gen_count']
            level = gen_count//10+1
            xp = gen_count%10
            embed=discord.Embed(title="유저 정보",description=f"<@{find.id}>", color=0xF3A4B5)
            embed.set_thumbnail(url=find.avatar.url)
            embed.add_field(name="모델", value=data['model'], inline=True)
            embed.add_field(name="VAE", value=f"kl-f8-anime2.ckpt", inline=True)
            embed.add_field(name="생성 횟수", value=gen_count, inline=True)
            embed.add_field(name=f"{level} 레벨 | XP : {xp} / {10}", value = ":green_square:"*(xp*2) + ':white_large_square:'*(20-xp*2))
            embed.set_footer(text="@bocchi#9621")
            await interaction.response.send_message(embed=embed)
        else:
            if user == None:
                await interaction.response.send_message(f"<@{find.id}>님은 아직 등록이 되어 있지 않아요!\n **/register** 으로 등록해주세요.",ephemeral=True)
            else:
                await interaction.response.send_message(f"<@{find.id}>님은 등록이 되어 있지 않아요!",ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        profile_(bot),
        guilds=[discord.Object(id=GUILD_ID)]
    )