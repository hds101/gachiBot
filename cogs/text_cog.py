import textwrap
import datetime

from discord.ext import commands
from lib.github import Github


class TextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def borda(self, ctx):
        await self.__last_commit(ctx, 'idesu', 'SoSnowyBoard')

    @commands.command()
    async def js(self, ctx):
        await self.__last_commit(ctx, 'Vitalyii', 'JS')

    @commands.command()
    async def gachibot(self, ctx):
        await self.__last_commit(ctx, 'hds101', 'gachiBot')

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

    async def __last_commit(self, ctx, author, repo):
        async with ctx.typing():
            commit = Github(author, repo).commits()[0]
        d = datetime.datetime.strptime(commit['commit']['committer']['date'],
                                       "%Y-%m-%dT%H:%M:%SZ")
        d_ago = (datetime.date.today() - d.date()).days
        message = textwrap.dedent(
            """
           ```
           Last update: {0} - {1} days ago
           Commit message: {2}
           ```
           {3}
           """
        ).format(d, d_ago, commit['commit']['message'], commit['html_url'])
        await ctx.send(message)
