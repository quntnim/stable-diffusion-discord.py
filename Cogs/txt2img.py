import discord
from discord import app_commands
from discord.ext import commands
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import asyncio
from var import *
from collections import deque

getimg_result = False
is_drawing = False
queue = deque()

class txt2img(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="txt2img")
    async def txt2img(
        self,  
        interaction: discord.Interaction, 
        prompt : str, 
        negative_prompt : str = "(low quality, worst quality:1.4), easynegative ,badhandv4, badv3, nsfw", 
        width : app_commands.Range[int,64,1024] = 384, 
        height : app_commands.Range[int,64,1024] = 512,
        steps : app_commands.Range[int,1,50] = 28,
        seed : int = -1,
        hires_toggle : bool = True
        ) -> None:
        """텍스트를 그림으로 만들어 줍니다.

        인자
        ----------
        prompt: str
            AI에게 그려야 할 것을 알려주는 문자열 입니다.
        negative_prompt: str
            AI에게 그리지 말아야 할 것을 알려주는 문자열 입니다. 기본값 - (low quality, worst quality:1.4), easynegative ,badhandv4, badv3, nsfw
        width: int
            이미지의 너비 입니다. (width는 64에서 1024 사이의 정수여야 합니다.) 기본값 - 384
        height: int
            이미지의 높이 입니다. (height는 64에서 1024 사이의 정수여야 합니다.) 기본값 - 512
        steps: int
            AI가 반복해서 그림을 그릴 횟수입니다 (steps는 1에서 50 사이의 정수여야 합니다.) 기본값 - 28
        seed : bool
            이미지 생성의 시드값을 정합니다 기본값 - -1
        hires_toggle : bool
            hires_fix의 온오프 여부를 정합니다. 기본값 - True
        """
        global is_drawing
        queued = False
        if is_drawing or len(queue):
            await interaction.response.send_message(f"다른 그림을 다 그릴때 까지 기다리는 중..")
            queue.append(interaction.id)
            queued = interaction.id
            while True:
                if not is_drawing and queue[0] == interaction.id:
                    queue.popleft()
                    break
                await interaction.edit_original_response(content = f"다른 그림을 다 그릴때 까지 기다리는 중.. **[ 대기열 : {queue.index(interaction.id)+1} ]**")
                await asyncio.sleep(1)
        is_drawing = True
    
        payload = {
            "enable_hr": hires_toggle,
            "denoising_strength": 0.4,
            "hr_scale": 2,
            "hr_second_pass_steps": 12,
            "firstphase_width": 0,
            "firstphase_height": 0,
            "hr_upscaler": "4x-AnimeSharp",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "sampler_index": "DPM++ 2M Karras",
            "sampler_name": "DPM++ 2M Karras",
            "steps": steps,
            "width": width,
            "height": height,
            "cfg_scale": 7,
            "seed": seed,
        }
        json_data = {}
        with open(JSON_PATH, "r") as json_file:
            json_data = json.load(json_file)
        user_cnt = len(json_data['users'])

        override_settings = {}
        for i in range(user_cnt):
            if interaction.user.id == json_data['users'][i]['userid']:
                json_data['users'][i]['gen_count'] += 1
                with open(JSON_PATH, 'w') as outfile:
                    json.dump(json_data, outfile, indent=4)

                override_settings['sd_model_checkpoint'] = json_data['users'][i]['model']
                override_payload = {"override_settings": override_settings}
                payload.update(override_payload)
                break
                
        if queued == interaction.id:await interaction.edit_original_response(content = f"그림 그리는 중..")
        else: await interaction.response.send_message(f"그림 그리는 중..")

        async def getimg():
            global response, getimg_result
            await asyncio.sleep(1)
            response = await asyncio.to_thread(requests.post,url=f'{url}/sdapi/v1/txt2img', json=payload)
            getimg_result = True
            return

        async def loop():
            while not getimg_result:
                progreq = requests.get(url=f'{url}/sdapi/v1/progress')
                prog = json.loads(progreq.text)
                perc = round(prog['progress']*100)
                eta = t if (t:=prog['eta_relative']) >= 0 else 0

                if perc == 1:await interaction.edit_original_response(content=f"그림 그리는 중.. **[ Model Loading.. | 예상 시간 : -초 ]**")
                else: await interaction.edit_original_response(content=f"그림 그리는 중.. **[ {perc}% | 예상 시간 : {eta:.1f}초 ]**\n ")
                if getimg_result:break
                await asyncio.sleep(0.1)
            await interaction.edit_original_response(content=f"그림 완성!")
            return

        async def process():
            global getimg_result
            getimg_result = False
            task1 = asyncio.create_task(getimg())
            task2 = asyncio.create_task(loop())
            await task1
            await task2
            return
        
        await process()
        

        r = response.json()
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save('output.png', pnginfo=pnginfo)
    
        res = discord.File("./output.png", filename="output.png")
        embed=discord.Embed(title=f"텍스트 -> 이미지",description=interaction.user.mention, color=0x4fff4a)
        embed.set_image(url="attachment://output.png")
        embed.add_field(name="프롬프트", value=prompt, inline=False)
        embed.add_field(name="네거티브", value=negative_prompt, inline=False)
        embed.set_footer(text="@bocchi#9621 이미지 생성")
        await interaction.edit_original_response(embed=embed,attachments=[res])
        is_drawing = False


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        txt2img(bot),
        guilds=[discord.Object(id=GUILD_ID)]
    )