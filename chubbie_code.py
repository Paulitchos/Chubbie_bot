import discord
from  discord.ext import commands
import random
import os
import re
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('bot_token')
bot_id = os.getenv('bot_id')
bot_client = commands.Bot(command_prefix='🍐')


"""===========================Bot Code here==========================="""
@bot_client.command()
async def hello(ctx):
    await ctx.send("I'm working bitches")

@bot_client.command()
async def leave(ctx):
    if ctx.voice_cliente:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Força aí meus putos")
    else:
        await ctx.send("Não estou num voice channel marmanjo")

@bot_client.event
async def on_raw_reaction_add(payload):
    random_pear = random.randrange(1,10)
    channel = bot_client.get_channel(payload.channel_id)
    message = await bot_client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    emoji =  payload.emoji #.name~
    print(message.author.id)
    print(bot_id)
    if message.author.id == int(bot_id):
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
""" elif str(emoji) == "🐴" and "cdn.discordapp.com/attachments" in message.content:
        for reaction in message.reactions:
            if str(reaction.emoji) == "🐴" and reaction.count == 1 and payload.author.voice:
                channel_voice = payload.message.author.voice.channel
                await channel_voice.connect()
                await message.add_reaction("🐴")
            else:
                await payload.send("Não estás em nenhum voice channel pepega") """












bot_client.run(bot_token)





