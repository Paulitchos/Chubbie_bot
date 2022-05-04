
import wavelink
import discord
import datetime
from wavelink.ext import spotify
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
        await wavelink.NodePool.create_node(bot=self.bot,host='lavalinkinc.ml',port=443,password= 'incognito',https=True,spotify_client=spotify.SpotifyClient(client_id=f"{self.bot.client_id_spotify}",client_secret=f"{self.bot.client_secret}"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self,node: wavelink.Node):
        print(f"Node {node.identifier} is ready")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self,player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)
        
        print("Track ended, next is playing = ",vc.is_playing())
        try:     
            next_song = vc.queue.get()
            await vc.play(next_song)
            await ctx.send(f"Agora a tocar: `{next_song.title}`")
        except:
            #An exception when after the track end, the queue is now empty. If you dont do this, it will get error.
            await vc.stop()
            print("Queue Empty and stopped, isplaying = ",vc.is_playing())

    @commands.command(name="pause",help ="Mete pausa na música a dar")
    async def pause(self,ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Não está a dar música")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.pause()
        await ctx.send("A música está parada")
    
    @commands.command(name="resume",aliases=["r","continue"],help ="Retoma a música || Alternativas 🍐r ou 🍐continue")
    async def resume(self,ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Não está a dar música")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.resume()
        await ctx.send("A música está de volta a dar")

    @commands.command(name="skip",help ="Dá skip à música")
    async def skip(self,ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Não está a dar música")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.stop()
        await ctx.send("Música skipped")

    @commands.command(name="stop",aliases=["s"],help ="Para de dar música || Alternativas 🍐s")
    async def stop(self,ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Não está a dar música")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.stop()
        await ctx.send("Parei a música e limpei o queue")
        vc.queue.clear()

    
    @commands.command(name="leave",aliases=["l","disconnect","d"],help ="Sái do voice channel || Alternativas 🍐l ou 🍐d ou 🍐disconnect")
    async def leave(self,ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Não estou num voice channel")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.disconnect()
        await ctx.send("Até mais Jake Paulers")

    @commands.command(name="loop",help ="Mete a música em loop")
    async def loop(self,ctx: commands.Context):
        if not ctx.voice_client:
            return ctx.send("Não está a dar música")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc,"loop",False)

        if vc.loop:
            return await ctx.send("Loop está ligado")
        else:
            return await ctx.send("Loop está desligado")

    @commands.command(name="queue", aliases =["q"],help ="Mostra o queue de músicas || Alternativas 🍐q")
    async def queue(self,ctx: commands.Context):
        if not ctx.voice_client:
            return ctx.send("Não está a dar música")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            return await ctx.send("Queue está vazio")

        em = discord.Embed(title = "Queue")
        queue = vc.queue.copy()
        song_count = 0
    
        for song in queue:
            song_count += 1
            em.add_field(name = f"Song Num {song_count}",value=f"`{song}`")

        return await ctx.send(embed=em)

    @commands.command(name="volume",aliases=["v","sound"],help ="Muda o volume do bot || Alternativas 🍐v ou 🍐sound")
    async def volume(self,ctx: commands.Context,volume: int):
        if not ctx.voice_client:
            return ctx.send("Não está a dar música")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client

        if volume > 100:
            return await ctx.send("Queres rebentar os ouvidos de quem camelo")
        elif volume < 0:
            return await ctx.send("Assim não se ouve nada tontche")
        
        await ctx.send(f"Volume a `{volume}%`")
        return await vc.set_volume(volume)

    @commands.command(name="now_playing",aliases=["np"],help ="Mostra o que está atualmente a tocar|| Alternativas 🍐np")
    async def now_playing(self,ctx: commands.Context):
        if not ctx.voice_client:
            return ctx.send("Não está a dar música")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Não estás no voice channel marmanjo")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if not vc.is_playing(): return await ctx.send("Não está a dar nada -.-")

        em = discord.Embed(title=f"Agora a tocar: {vc.track.title}",description=f"Artista: {vc.track.author}")
        em.add_field(name="Duração",value = f"`{str(datetime.timedelta(seconds=vc.track.length))}`")
        em.add_field(name="Informação Extra", value=f"Música URL: [CLICA AQUI]({str(vc.track.uri)})")
        
        return await ctx.send(embed=em)

    @commands.command(name="play", aliases=["p","playing"],help ="Mete música a dar || Alternativas 🍐p ou 🍐playing")
    async def play(self,ctx: commands.Context, *, search: str):
        
        if not getattr(ctx.author.voice,"channel",None):
            return await ctx.send("Entra num voice channel pepega")

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            tracks = await spotify.SpotifyTrack.search(query = search)
        except:
            tracks = await spotify.YouTubeTrack.search(query = search)

        track = tracks[0]

        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(track)  
            await ctx.send(f"Agora a tocar `{track.title}`")
        else:
            await vc.queue.put_wait(track)
            await ctx.send(f"Música adicionada ao queue")

        vc.ctx = ctx
        setattr(vc,"loop",False)