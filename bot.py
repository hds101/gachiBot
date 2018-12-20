import discord
import json
import random
import os
import youtube_dl

"""
!comeon - move to current channel
!fuckyou - disconnect
!gachi - stop current song, play random gachi
!takeitboy - move to parasha
"""


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

ydl_opts = {'format': 'bestaudio/best'}
with open('songs.json') as json_data:
    songs = json.load(json_data)

client = discord.Client()


@client.event
async def on_ready():
    game = discord.Game("gachiBASS")
    await client.change_presence(activity=game)
    print('Logged on as {0}!'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        await message.channel.send(
            "```" +
            "!comeon - move to current channel\n" +
            "!gachi - stop current song, play random gachi\n" +
            "!takeitboy - move to parasha\n" +
            "!fuckyou - disconnect" +
            "```"
        )

    elif message.content.startswith('<!'):
        sosna = message.guild.get_member(188000465550573569)
        await message.channel.send('{}, https://github.com/Vitalyii/JS/commit/780f5440e2114ec86872bff991082d2a88deb39a'.format(sosna.mention))

    elif message.content.startswith('!comeon'):
        channel = message.author.voice.channel
        if channel.guild.voice_client:
            voice_client = channel.guild.voice_client
            await voice_client.move_to(channel)
        else:
            await channel.connect()

        await message.channel.send('Oh yeah? I\'ll kick your ass!')

    elif message.content.startswith('!fuckyou'):
        channel = message.author.voice.channel
        if channel.guild.voice_client:
            voice_client = channel.guild.voice_client
            await message.channel.send(
                'Oh, fuck you leather man.'
            )
            await voice_client.disconnect()

    elif message.content.startswith('!takeitboy'):
        channel = message.author.voice.channel
        if channel != channel.guild.afk_channel:
            voice_client = channel.guild.voice_client
            await voice_client.move_to(channel.guild.afk_channel)

    elif message.content.startswith('!gachi'):
        channel = message.author.voice.channel
        if channel.guild.voice_client:
            voice_client = channel.guild.voice_client
        else:
            voice_client = await channel.connect()

        if voice_client.is_playing():
            voice_client.stop()

        song = random.SystemRandom().choice(songs)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                'https://www.youtube.com/watch?v={}'.format(song['url']),
                download=False
            )
            audio_url = info['formats'][0]['url']

            await message.channel.send('Now playing: {}'.format(song['title']))
            voice_client.play(discord.FFmpegPCMAudio(audio_url))


client.run(os.environ['GACHIBOT_TOKEN'])
