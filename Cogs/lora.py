import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select
from discord import ButtonStyle
import json
import requests
import io
import base64
import os
from PIL import Image, PngImagePlugin
from var import *
import math
import asyncio

lora_is_selected = {}
class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

class lora(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="lora")
    async def lora(self, interaction: discord.Interaction, query : str) -> None:
        """서버에 있는 로라를 검색합니다. (beta)

        인자
        ----------
        query: str
            검색할 로라의 키워드 입니다.
        """ 
        global page_now, lora_is_selected
        lora_is_selected[interaction.user.id] = False
        data = []
        for (r,d,files) in os.walk(LORA_PATH):
            for file in files:
                if query.lower() in file.lower() and '.safetensors' in file:
                    temp = os.path.join(r, file).replace('.safetensors','')
                    data.append((file,temp))
        lora_cnt = len(data)
        if not lora_cnt:
            await interaction.response.send_message(content='로라가 검색되지 않았어요.', ephemeral=True)
            return
        page_lim = math.ceil(lora_cnt/25)
        page_now = 1
        
        def selectmake():
            global loralist
            selop = []
            for i in range(25*(page_now-1),25*page_now):
                if i == lora_cnt:break
                selop.append(discord.SelectOption(label=f"{data[i][0]}", value=i))
            return selop


        # UI 선언 및 콜백 함수
        if query != None:
            selects = Select(options=selectmake(),placeholder=f'로라 선택하기  |  검색 쿼리 : {query}')
        else:
            selects = Select(options=selectmake(),placeholder='로라 선택하기')
        left = Button(label='<<', style=ButtonStyle.primary)
        right = Button(label='>>', style=ButtonStyle.primary)
        page = Button(label = f'{page_now}/{page_lim}', style=ButtonStyle.grey, disabled=True)
        cancel = Button(label='X', style=ButtonStyle.red)
        
        async def select_callback(interaction : discord.Interaction) -> None:
            global lora_is_selected
            select_val = int(selects.values[0])
            lora_is_selected[interaction.user.id] = select_val

            embed=discord.Embed(title=f"{data[select_val][0]} 로라의 정보에요", color=0x4fff4a)
            embed.set_footer(text="@bocchi#9621")
            embed.add_field(name="프롬프트", value=f'<lora:{data[select_val][0].replace(".safetensors","")}:0.9>',inline=False)

            try:
                txt = open(f"{data[select_val][1]}.txt",'r',encoding='UTF-8')
                info = []
                for line in txt.readlines():
                    info.append(line)

                embed.add_field(name="설명", value=''.join(info),inline=False)
            except:
                embed.add_field(name="설명", value='설명이 없어요.',inline=False)

            try:
                res = discord.File(f"{data[select_val][1]}.png", filename=f"lora_preview.png")
                embed.set_thumbnail(url=f"attachment://lora_preview.png")
                await interaction.response.edit_message(view=view_make(), embed=embed ,attachments=[res])
            except:
                await interaction.response.edit_message(view=view_make(), embed=embed ,attachments=[])


        async def left_callback(interaction : discord.Interaction):
            global page_now
            if page_now != 1:page_now-=1
            await interaction.response.edit_message(view=view_make())

        async def right_callback(interaction : discord.Interaction):
            global page_now
            if page_now != page_lim:page_now+=1
            await interaction.response.edit_message(view=view_make())

        async def page_callback(interaction : discord.Interaction):
            global lora_is_selected
            lora_is_selected[interaction.user.id] = False
            await interaction.response.edit_message(content='Todo: 페이지 한번에 이동하기', view=view_make())

        async def cancel_callback(interaction : discord.Interaction):
            embed=discord.Embed(title=f"로라 검색을 취소했어요.",description=f"이 메시지는 3초 후에 {DEL_MESSAGE[interaction.id%6]}.", color=0xca474c)
            embed.set_footer(text="@bocchi#9621")
            await interaction.response.edit_message(view=View() , embed=embed ,attachments=[])
            await asyncio.sleep(3)
            await interaction.delete_original_response()
        
        selects.callback = select_callback
        left.callback = left_callback
        right.callback = right_callback
        page.callback = page_callback
        cancel.callback = cancel_callback

        def view_make():
            left.disabled = True if page_now == 1 else False
            right.disabled = True if page_now == page_lim else False
            page.label = f"{page_now} / {page_lim}"

            view = View()
            selects.options = selectmake()
            view.add_item(selects)
            view.add_item(left)
            view.add_item(page)
            view.add_item(right)
            view.add_item(cancel)
            return view

        embed=discord.Embed(title=f"아래 선택 메뉴에서 찾을 로라를 골라 주세요.", color=0x777777)
        embed.set_footer(text="@bocchi#9621")
        await interaction.response.send_message(embed=embed, view=view_make(), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        lora(bot),
        guilds=[discord.Object(id=GUILD_ID)]
    )