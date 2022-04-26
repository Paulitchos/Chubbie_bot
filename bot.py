from pathlib import Path
from dotenv import load_dotenv
import os
import discord


from discord.ext import commands
load_dotenv()
bot_token = os.getenv('bot_token')




class Bot(commands.Bot):
    def __init__(self):
        print(os.getcwd())
        self.prefix = "🍐"
        self.__cogs = [p.stem for p in Path(".").glob("./cogs/*.py")]
        super().__init__(command_prefix = self.prefix, case_insensitive = True, intents = discord.Intents.all())
        self.bot_id = os.getenv('bot_id')
        self.client_id_spotify = os.getenv('client_id')
        self.client_secret = os.getenv('client_secret')

    def run(self):
        self.__load_cogs()

        super().run(bot_token, reconnect = True)


    def __load_cogs(self):
        for cog in self.__cogs:
            self.load_extension(f"cogs.{cog}")
            print(f"Loaded cog = {cog}")


    async def on_ready(self):
        self.client_id = (await self.application_info()).id