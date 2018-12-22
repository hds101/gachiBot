from discord.ext import commands


class TextBot:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def zaebat(self, ctx):
        """ Zaebat' sosninu """

        sosna = ctx.guild.get_member(188000465550573569)
        await ctx.send('И охуенен 👉 {}'.format(sosna.mention))

    @commands.command()
    async def pubg(self, ctx):
        """ Let's play some pubg """
        pass

    @commands.command()
    async def pupk(self, ctx):
        """ !pubg alias """
        pass

    @pubg.before_invoke
    @pupk.before_invoke
    async def __pubg(self, ctx):
        gav = self.bot.get_emoji(485168219926167555)
        await ctx.send('{0} {0} {0}'.format(gav))
