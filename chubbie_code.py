import discord
from  discord.ext import commands
import random

bot_token = "OTUxMjU1NzY2Mzk0ODkyMzc5.Yikz-A.NYyqmhEAup1hmoQVSIE_dRU_Nf8"
bot_client = commands.Bot(command_prefix='🍐')

"""===========================Bot Code here==========================="""
@bot_client.command()
async def hello(ctx):
    await ctx.send("I'm working bitches")

@bot_client.event
async def on_raw_reaction_add(payload):
    
    random_pear = random.randrange(1,10)
    channel = bot_client.get_channel(payload.channel_id)
    message = await bot_client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    emoji =  payload.emoji #.name
    if message.author.id == 951255766394892379:
        return
    if str(emoji) == "🍐" and "cdn.discordapp.com/attachments" in message.content:
        for reaction in message.reactions:
            if str(reaction.emoji) == "🍐" and reaction.count == 1:
                await channel.send(f"{message.content}\nFat Pear Meter {random_pear * '🍐'}/🍐🍐🍐🍐🍐🍐🍐🍐🍐🍐" )
                await message.add_reaction("🍐")















bot_client.run(bot_token)





