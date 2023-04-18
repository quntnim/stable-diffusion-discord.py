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

class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

class set_model(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="set-model")
    async def set_model(self, interaction: discord.Interaction) -> None:
        global page_now
        """현재 설정되있는 모델을 바꿉니다.
        """ 
        # 첫 변수 선언
        response = requests.get(url=f'{url}/sdapi/v1/sd-models')
        data = json.loads(response.text)
        model_cnt = len(data)
        page_lim = math.ceil(model_cnt/25)
        page_now = 1

        def selectmake():
            selop = []
            for i in range(25*(page_now-1),25*page_now):
                if i > model_cnt:break
                selop.append(discord.SelectOption(label=f"{data[i]['model_name']}"))
            return selop


        # UI 선언 및 콜백 함수
        selects = Select(options=selectmake())
        left = Button(label='<<', style=ButtonStyle.primary)
        right = Button(label='>>', style=ButtonStyle.primary)
        page = Button(label = f'{page_now}/{page_lim}', style=ButtonStyle.grey)
        
        async def select_callback(interaction : discord.Interaction) -> None:
            await interaction.response.edit_message(content=f'{selects.values} 선택.', view=view_make())
        async def left_callback(interaction : discord.Interaction):
            global page_now
            if page_now != 1:page_now-=1
            await interaction.response.edit_message(content='<<', view=view_make())
        async def right_callback(interaction : discord.Interaction):
            global page_now
            if page_now != page_lim:page_now+=1
            await interaction.response.edit_message(content='>>', view=view_make())
        async def page_callback(interaction : discord.Interaction):
            await interaction.response.edit_message(content='Todo: 페이지 한번에 이동하기', view=view_make())

        selects.callback = select_callback
        left.callback = left_callback
        right.callback = right_callback
        page.callback = page_callback

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
            return view

        await interaction.response.send_message(f"버튼?", view=view_make())
        
        # option_payload = {
        #     "sd_model_checkpoint":model
        # }
        # response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)
        # await interaction.edit_original_response(content=f"모델을 {model}으로 설정했어요!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        set_model(bot),
        guilds=[discord.Object(id=guildid)]
    )