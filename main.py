import discord
from discord.ext import commands
from var import *

class SD_Bocchi(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            sync_command=True,
            application_id=APP_ID
        )
        self.inital_extension = [
            "Cogs.ping",
            "Cogs.memory",
            "Cogs.profile_",
            "Cogs.register",
            "Cogs.set-model",
            "Cogs.txt2img",

        ]
        
    async def setup_hook(self):
        for ext in self.inital_extension:
            await self.load_extension(ext)
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        # await bot.tree.sync()


    async def on_ready(self):
        print('로그인 됨')
        print(self.user.name)
        print(self.user.id)
        print('---------------')
        activity = discord.Game("돚거")
        await self.change_presence(status=discord.Status.online, activity=activity)














bot = SD_Bocchi()
bot.run(TOKEN)