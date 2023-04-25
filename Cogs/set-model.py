import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select
from discord import ButtonStyle
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from var import *
import math
import asyncio

is_selected = {}
class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

class set_model(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="set-model")
    async def set_model(self, interaction: discord.Interaction, query : str = None) -> None:
        """현재 설정되있는 모델을 바꿉니다.

        인자
        ----------
        query: str
            검색할 모델 명을 알려주는 문자열 입니다. 기본값 - None
        """ 
        global page_now, is_selected
        is_selected[interaction.user.id] = False
        response = requests.get(url=f'{url}/sdapi/v1/sd-models')
        data = json.loads(response.text)
        if query != None:
            q = query.lower()
            temp = []
            for i in data:
                if q in i['model_name'].lower():temp.append(i)
            data = temp
        
        model_cnt = len(data)
        if not model_cnt:
            await interaction.response.send_message(content='모델이 검색되지 않았어요.', ephemeral=True)
            return
        page_lim = math.ceil(model_cnt/25)
        page_now = 1
        
        def selectmake():
            selop = []
            for i in range(25*(page_now-1),25*page_now):
                if i == model_cnt:break
                selop.append(discord.SelectOption(label=f"{data[i]['model_name']}", description=f"{data[i]['hash']}"))
            return selop


        # UI 선언 및 콜백 함수
        if query != None:
            selects = Select(options=selectmake(),placeholder=f'모델 선택하기  |  검색 쿼리 : {query}')
        else:
            selects = Select(options=selectmake(),placeholder='모델 선택하기')
        left = Button(label='<<', style=ButtonStyle.primary)
        right = Button(label='>>', style=ButtonStyle.primary)
        page = Button(label = f'{page_now}/{page_lim}', style=ButtonStyle.grey, disabled=True)
        approve = Button(label='✅', style=ButtonStyle.green)
        cancel = Button(label='X', style=ButtonStyle.red)
        
        async def select_callback(interaction : discord.Interaction) -> None:
            global is_selected
            is_selected[interaction.user.id] = ''.join(selects.values)
            embed=discord.Embed(title=f"{is_selected[interaction.user.id]}", color=0x4fff4a)
            embed.set_author(name=f"{is_selected[interaction.user.id]} 모델로 바꿀까요?")
            embed.set_footer(text="@bocchi#9621")
            try:
                res = discord.File(f"{MODEL_PATH}{is_selected[interaction.user.id]}.png", filename=f"{is_selected[interaction.user.id]}.png")
                embed.set_image(url=f"attachment://{is_selected[interaction.user.id]}.png")
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
            global is_selected
            is_selected[interaction.user.id] = False
            await interaction.response.edit_message(content='Todo: 페이지 한번에 이동하기', view=view_make())

        async def approve_callback(interaction : discord.Interaction):
            embed=discord.Embed(title=f'**{is_selected[interaction.user.id]}** 모델으로 설정할게요.', color=0x777777)
            embed.set_footer(text="@bocchi#9621")
            await interaction.response.edit_message(embed=embed,view=View(),attachments=[])

            json_data = {}
            with open(JSON_PATH, "r") as json_file:
                json_data = json.load(json_file)
            user_cnt = len(json_data['users'])

            is_exist = False
            for i in range(user_cnt):
                if interaction.user.id == json_data['users'][i]['userid']:
                    is_exist = True
                    json_data['users'][i]['model'] = is_selected[interaction.user.id]
                    break
            
            if not is_exist:
                json_data['users'].append({
                    "userid": interaction.user.id,
                    "model": is_selected[interaction.user.id]
                })
            
            with open(JSON_PATH, 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            embed.title = f"**{is_selected[interaction.user.id]}** 모델으로 설정했어요!"
            is_selected.pop(interaction.user.id)
            await interaction.edit_original_response(embed=embed)

        async def cancel_callback(interaction : discord.Interaction):
            embed=discord.Embed(title=f"모델 변경을 취소했어요.", color=0xca474c)
            embed.set_footer(text="@bocchi#9621")
            await interaction.response.edit_message(view=View() , embed=embed ,attachments=[])
        
        selects.callback = select_callback
        left.callback = left_callback
        right.callback = right_callback
        page.callback = page_callback
        approve.callback = approve_callback
        cancel.callback = cancel_callback

        def view_make():
            left.disabled = True if page_now == 1 else False
            right.disabled = True if page_now == page_lim else False
            approve.disabled = True if is_selected[interaction.user.id] == False else False
            page.label = f"{page_now} / {page_lim}"

            view = View()
            selects.options = selectmake()
            view.add_item(selects)
            view.add_item(left)
            view.add_item(page)
            view.add_item(right)
            view.add_item(approve)
            view.add_item(cancel)
            return view

        embed=discord.Embed(title=f"아래 선택 메뉴에서 모델을 골라 주세요.", color=0x777777)
        embed.set_footer(text="@bocchi#9621")
        await interaction.response.send_message(embed=embed, view=view_make(), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        set_model(bot),
        guilds=[discord.Object(id=GUILD_ID)]
    )