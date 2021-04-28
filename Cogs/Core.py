import discord
from discord.ext import commands
from random import choice


cog_list = ['기본', '유틸']


class Core(commands.Cog, name='기본'):

    def __init__(self, client):
        self.client = client

    @commands.command(name='안녕', help="타봇이랑 인사해요. ", usage="!타봇 안녕")
    async def Hello(self, ctx):

        cmt = ["싸대기 탁! 야추 탁! 야꼭지 탁!", "응 싸대기 쳐맞어 그냥 쳐맞어 존나 쳐맞어"]
        await ctx.send(f"{ctx.author.name}님 안녕하세요? " + choice(cmt))

    @commands.command()
    async def test(self, ctx):

        print(dir(ctx.author))
        print(ctx.author.id, ctx.author.name, ctx.author.nick)

    @commands.command(name='도움말', help="타봇 카테고리별 명령어 가이드를 보여줘요.", usage="!타봇 도움말 <command>")
    async def Help(self, ctx, func=None):

        if func is None:
            embed = discord.Embed(title="타봇 명령어 가이드",
                                  description=None)
            for x in cog_list:
                cog_data = self.client.get_cog(x)  # x에 대해 Cog 데이터를 구하기
                command_list = cog_data.get_commands()  # cog_data에서 명령어 리스트 구하기
                embed.add_field(name=x, value=" ".join(
                    [c.name+"\n" for c in command_list]), inline=True)  # 필드 추가
            await ctx.send(embed=embed)
        else:  # func가 None이 아니면
            command_notfound = True
            # title, cog로 item을 돌려주는데 title은 필요가 없습니다.
            for _, cog in self.client.cogs.items():
                if not command_notfound:  # False면
                    break
                else:  # 아니면
                    for title in cog.get_commands():  # 명령어를 아까처럼 구하고 title에 순차적으로 넣습니다.
                        if title.name == func:  # title.name이 func와 같으면
                            # title의 명령어 데이터를 구합니다.
                            cmd = self.client.get_command(title.name)
                            embed = discord.Embed(
                                title=f"명령어 : {cmd}", description=cmd.help)  # Embed 만들기
                            embed.add_field(
                                name="사용법", value=cmd.usage)  # 사용법 추가
                            await ctx.send(embed=embed)  # 보내기
                            command_notfound = False
                            break  # 반복문 나가기
                        else:
                            command_notfound = True

            if command_notfound:
                if func in cog_list:  # 만약 cog_list에 func가 존재한다면
                    cog_data = self.client.get_cog(func)  # cog 데이터 구하기
                    command_list = cog_data.get_commands()  # 명령어 리스트 구하기
                    embed = discord.Embed(
                        title=f"카테고리 : {cog_data.qualified_name}", description=cog_data.description)  # 카테고리 이름과 설명 추가
                    embed.add_field(name="명령어들", value=", ".join(
                        [c.name for c in command_list]))  # 명령어 리스트 join
                    await ctx.send(embed=embed)  # 보내기
                else:
                    await ctx.send("없어")


def setup(client):
    client.add_cog(Core(client))
