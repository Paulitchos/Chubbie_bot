import wavelink

from discord.ext import commands

def setup(bot : commands.Bot):
    bot.add_cog(music_code(bot))

class music_code(commands.Cog):
    def __init__(self, bot_client):
        print("Bot is ready")
        self.bot = bot_client
        self.bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot,host='lavalinkinc.ml',port=443,password= 'incognito',https=True)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self,node: wavelink.Node):
        print(f"Node {node.identifier} is ready")

    @commands.command(name="play", aliases=["p","playing"])
    async def play(self,ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice,"channel",None):
            return await ctx.send("Entra num voice channel pepega")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.play(search)


