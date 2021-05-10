import discord
from discord.ext import commands
from random import randrange
from random import choice


class Game(commands.Cog, name='게임'):

    def __init__(self, client):
        self.client = client

    @commands.command(name='로또', help="로또 번호 생성기 ", usage="!타봇 로또")
    async def Lotto(self, ctx):

        lotto_num = []
        for x in range(1, 7):
            lotto_num.append(randrange(1, 46))

        await ctx.send(lotto_num)

    @commands.command(name='가위바위보', help="가위 바위 보 ", usage="!타봇 가위바위보")
    async def GBB(self, ctx):
        await ctx.send("제작중")

    @commands.command(name='사다리', help="사다리 타기 ", usage="!타봇 사다리")
    async def Ladder(self, ctx):
        await ctx.send("제작중")

    @commands.command(name='투표', help="투표 ", usage="!타봇 투표 <args...>")
    async def Vote(self, ctx):
        await ctx.send("제작중")


def setup(client):
    client.add_cog(Game(client))
