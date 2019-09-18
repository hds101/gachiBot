import discord
import json
import random

from discord.ext import commands
from lib.youtube import YTDLSource


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.volume_lvl = 0.5

        with open('assets/song_list.json') as json_data:
            self.gachi_list = json.load(json_data)

    @commands.command()
    async def gachi(self, ctx):
        """ Plays a song from the gachi list """

        song = random.choice(self.gachi_list)
        url = 'https://www.youtube.com/watch?v={}'.format(song['url'])
        await self.__yt(ctx, url)

    @commands.command()
    async def yt(self, ctx, *, url):
        """ Play from the given url / search for a song """

        await self.__yt(ctx, url)

    @commands.command()
    async def rv(self, ctx, *, url):
        """ Always right version """

        rv_url = "{} right version".format(url)
        await self.__yt(ctx, rv_url)

    @commands.command()
    async def pause(self, ctx):
        """ Pauses current track """

        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """ Resumes current track """

        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume """

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        self.volume_lvl = volume / 100
        ctx.voice_client.source.volume = self.volume_lvl
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def fuckyou(self, ctx):
        """ Stops and disconnects the bot from voice """

        sosna = ctx.guild.get_member(188000465550573569)
        if ctx.author == sosna:
            return await ctx.send('Oh, fuck you leather man')

        await ctx.voice_client.disconnect()

    @gachi.before_invoke
    @yt.before_invoke
    @rv.before_invoke
    async def __ensure_voice(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel.")

        channel = ctx.author.voice.channel
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            return await ctx.voice_client.move_to(channel)

        await channel.connect(reconnect=True)

    async def __yt(self, ctx, url, silent=False):
        if ctx.voice_client is None:
            return

        async with ctx.typing():
            player = await YTDLSource.from_url(
                url,
                loop=self.bot.loop,
                stream=False,
                volume=self.volume_lvl
            )
            ctx.voice_client.play(
                player,
                after=lambda e: print('Player error: %s' % e) if e else None
            )

        if not silent:
            await ctx.send(
                'Now playing: {0} [{1}]'.format(player.title, player.time)
            )
