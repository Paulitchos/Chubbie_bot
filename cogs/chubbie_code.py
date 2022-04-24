from discord.ext import commands
import random
import re

def setup(bot : commands.Bot):
    bot.add_cog(chubbie_code(bot))


    
class chubbie_code(commands.Cog):
    def __init__(self, bot_client):
        print("Bot is ready")
        self.bot = bot_client

    @commands.command(name="hello")
    async def hello(self,ctx):
        await ctx.send("I'm working bitches")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        random_pear = random.randrange(1,10)
        channel = self.bot.get_channel(payload.channel_id)
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        emoji =  payload.emoji #.name~
        if message.author.id == int(self.bot.bot_id):
            return
        if str(emoji) == "🍐":
            for attachment in message.attachments:
                if (".png" in attachment.filename or ".jpeg" in attachment.filename or  ".gif" in attachment.filename or ".jpg" in attachment.filename):
                    for reaction in message.reactions:
                        if str(reaction.emoji) == "🍐" and reaction.count == 1:
                            await channel.send(f"{attachment.url}\nFat Pear Meter {random_pear * '🍐'}/🍐🍐🍐🍐🍐🍐🍐🍐🍐🍐" )
                            await message.add_reaction("🍐")
            if (re.search("http(s)?:\/\/[a-z0-9\-\.]+\.[a-z]+\/([a-z0-9\/])+\.(png|gif|jpeg|jpg)",message.content)):
                for reaction in message.reactions:
                        if str(reaction.emoji) == "🍐" and reaction.count == 1:
                            await channel.send(f"{message.content}\nFat Pear Meter {random_pear * '🍐'}/🍐🍐🍐🍐🍐🍐🍐🍐🍐🍐" )
                            await message.add_reaction("🍐")






