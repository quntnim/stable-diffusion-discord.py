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

class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

class set_model(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="set-model")
    async def set_model(self, interaction: discord.Interaction) -> None:
        """현재 설정되있는 모델을 바꿉니다.
        """ 
        global page_now, is_selected
        is_selected = False
        response = requests.get(url=f'{url}/sdapi/v1/sd-models')
        data = json.loads(response.text)
        model_cnt = len(data)
        page_lim = math.ceil(model_cnt/25)
        page_now = 1
        
        def selectmake():
            selop = []
            for i in range(25*(page_now-1),25*page_now):
                if i == model_cnt-1:break
                selop.append(discord.SelectOption(label=f"{data[i]['model_name']}", description=f"{data[i]['hash']}"))
            return selop


        # UI 선언 및 콜백 함수
        selects = Select(options=selectmake())
        left = Button(label='<<', style=ButtonStyle.primary)
        right = Button(label='>>', style=ButtonStyle.primary)
        page = Button(label = f'{page_now}/{page_lim}', style=ButtonStyle.grey, disabled=True)
        approve = Button(label='✅', style=ButtonStyle.green)
        cancel = Button(label='X', style=ButtonStyle.red)
        
        async def select_callback(interaction : discord.Interaction) -> None:
            global is_selected
            is_selected = ''.join(selects.values)
            await interaction.response.edit_message(content=f'**{is_selected}** 모델로 바꿀까요?', view=view_make())

        async def left_callback(interaction : discord.Interaction):
            global page_now
            if page_now != 1:page_now-=1
            if is_selected:
                await interaction.response.edit_message(content=f'**{is_selected}** 모델로 바꿀까요?', view=view_make())
            else:
                await interaction.response.edit_message(content='어떤 모델로 바꿀까요?', view=view_make())

        async def right_callback(interaction : discord.Interaction):
            global page_now
            if page_now != page_lim:page_now+=1
            if is_selected:
                await interaction.response.edit_message(content=f'**{is_selected}** 모델로 바꿀까요?', view=view_make())
            else:
                await interaction.response.edit_message(content='어떤 모델로 바꿀까요?', view=view_make())

        async def page_callback(interaction : discord.Interaction):
            global is_selected
            is_selected = False
            await interaction.response.edit_message(content='Todo: 페이지 한번에 이동하기', view=view_make())

        async def approve_callback(interaction : discord.Interaction):
            await interaction.response.edit_message(content=f'**{is_selected}** 모델으로 설정할게요.', view=View())
            json_data = {}
            with open(json_path, "r") as json_file:
                json_data = json.load(json_file)
            user_cnt = len(json_data['users'])

            is_exist = False
            for i in range(user_cnt):
                if interaction.user.id == json_data['users'][i]['userid']:
                    is_exist = True
                    json_data['users'][i]['model'] = is_selected
                    break
            
            if not is_exist:
                json_data['users'].append({
                    "userid": interaction.user.id,
                    "model": is_selected
                })
            
            with open(json_path, 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            await interaction.edit_original_response(content=f"**{is_selected}** 모델으로 설정했어요!")

        async def cancel_callback(interaction : discord.Interaction):
            await interaction.response.edit_message(content=f'모델 변경을 취소했어요.',view=View())
        
        selects.callback = select_callback
        left.callback = left_callback
        right.callback = right_callback
        page.callback = page_callback
        approve.callback = approve_callback
        cancel.callback = cancel_callback

        def view_make():
            left.disabled = True if page_now == 1 else False
            right.disabled = True if page_now == page_lim else False
            approve.disabled = True if is_selected == False else False
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

        await interaction.response.send_message(f"어떤 모델로 바꿀까요?", view=view_make())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        set_model(bot),
        guilds=[discord.Object(id=guildid)]
    )