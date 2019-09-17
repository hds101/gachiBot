import os
import discord
from discord.ext import commands

from cogs.music_cog import MusicCog
from cogs.text_cog import TextCog
from cogs.event_cog import EventCog


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description='gachiBASS Clap'
)

bot.add_cog(MusicCog(bot))
bot.add_cog(TextCog(bot))
bot.add_cog(EventCog(bot))


bot.run(os.environ['GACHIBOT_TOKEN'])
