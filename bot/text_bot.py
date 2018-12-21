from discord.ext import commands


class TextBot:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def zaebat(self, ctx):
        """ Zaebat' sosninu """

        sosna = ctx.guild.get_member(188000465550573569)
        await ctx.send(sosna.mention)
