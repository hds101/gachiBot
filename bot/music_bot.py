import discord
import json
import random

from discord.ext import commands
from .ytdl import YTDLSource

with open('song_list.json') as json_data:
    songs = json.load(json_data)


class MusicBot:
    def __init__(self, bot):
        self.bot = bot
        self.volume_lvl = 0.5

    @commands.command()
    async def comeon(self, ctx, *, channel: discord.VoiceChannel=None):
        """ Joins a voice channel """

        if channel is None and ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel.")

        channel = channel or ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

    @commands.command()
    async def gachi(self, ctx):
        """ Plays a song from the gachi list """

        async with ctx.typing():
            song = random.SystemRandom().choice(songs)
            url = 'https://www.youtube.com/watch?v={}'.format(song['url'])
            player = await YTDLSource.from_url(
                url,
                loop=self.bot.loop,
                stream=True,
                volume=self.volume_lvl
            )
            ctx.voice_client.play(
                player,
                after=lambda e: print('Player error: %s' % e) if e else None
            )

        await ctx.send(
            'Now playing: {0} [{1}]'.format(player.title, player.time)
        )

    @commands.command()
    async def yt(self, ctx, *, url):
        """ Play from the given url / search for a song """

        async with ctx.typing():
            player = await YTDLSource.from_url(
                url,
                loop=self.bot.loop,
                stream=True,
                volume=self.volume_lvl
            )
            ctx.voice_client.play(
                player,
                after=lambda e: print('Player error: %s' % e) if e else None
            )

        await ctx.send(
            'Now playing: {0} [{1}]'.format(player.title, player.time)
        )

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
    async def __ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
