import discord
from discord import app_commands
from discord.ext import commands
import json
from var import *

class rank(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="rank")
    async def rank(self, interaction: discord.Interaction) -> None:
        """서버의 유저 랭킹을 보여줍니다."""
        json_data = {}
        with open(JSON_PATH, "r") as json_file:
            json_data = json.load(json_file)
        user_cnt = len(json_data['users'])

        data = []
        for i in range(user_cnt):
            data.append((json_data['users'][i]['userid'],json_data['users'][i]['gen_count']))
        data.sort(key=lambda x: -x[1])

        res = ''
        for idx, temp in enumerate(data):
            res += f'{idx+1}등 - <@{temp[0]}> {temp[1]}\n'
        embed=discord.Embed(title="랭킹", color=0xF3A4B5)
        embed.add_field(name="생성 횟수", value=''.join(res), inline=True)
        embed.set_footer(text="@bocchi#9621")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        rank(bot),
        guilds=[discord.Object(id=GUILD_ID)]
    )