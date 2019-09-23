import discord
from discord.ext import commands


class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as:\n{0} (ID: {0.id})'.format(self.bot.user))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        await channel.send(file=discord.File('assets/welcome.jpg'))
        await channel.send('Welcome to the club, buddy!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if '<:gav:485168219926167555>' in message.content:
            gav = self.bot.get_emoji(485168219926167555)
            await message.channel.send('{0} {0} {0}'.format(gav))
