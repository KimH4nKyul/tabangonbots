from asyncio.windows_events import NULL
import os
import discord
from discord.ext import commands
import requests


class Utils(commands.Cog, name='유틸'):

    def __init__(self, client):
        self.client = client

    def serchIndex(self, v: str):

        my_lang = ['한국어', '영어', '참깨어',
                   '대만어', '스페인어', '프랑스어', '베트남어', '태국어', '인도네시아어']
        support_lang = ['ko', 'en', 'zh-CN',
                        'zh-TW', 'es', 'fr', 'vi', 'th', 'id']

        res: str = ''
        if v in my_lang:
            res = support_lang[my_lang.index(v)]
        else:
            return IndexError

        return res

    @commands.command(name="번역", help="", usage="!타봇 번역 <기준어> <번역어> <문장>")
    async def Translate(self, ctx, src, dst, *msg):

        papago_client_id = os.environ.get('papagoid')
        papago_client_secret = os.environ.get('papagosecret')

        text = ''
        for x in msg:
            text = text + x + " "
        print(text)

        source = self.serchIndex(src)
        target = self.serchIndex(dst)

        request_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers = {"X-Naver-Client-Id": papago_client_id,
                   "X-Naver-Client-Secret": papago_client_secret}
        data = {'source': source,
                'target': target,
                'text': text.encode('utf-8')}

        res = requests.post(request_url, data=data, headers=headers)
        if res.status_code == 200:
            res_body = res.json()
            await ctx.send(res_body['message']['result']['translatedText'])
        else:
            await ctx.send("번역할 수 없습니다. ", res.status_code, " 에러 발생!")
            # print(res.status_code)
            return

        res.close()

    @commands.command(name='카카오맵', help="카카오맵으로 장소 검색하기", usage="!타봇 카카오맵 <주소 | 건물명>")
    async def KakaoMap(self, ctx):

        await ctx.send("카카오맵 기능은 테스트중에 있습니다. 조만간 서비스 해드릴게요~")

    @commands.command(name='코인', help="코인 관련 정보를 크롤링해 보여줘요. ", usage="!타봇 코인 <유튜브 | 뉴스>")
    async def Coin(self, ctx):

        await ctx.send("\n코인 기능은 유튜브 | 뉴스 정보만을 제공할 뿐 개인정보와 관련된 트레이딩 기능은 제공하지 않습니다. \n그외 OPEN API(업비트, 바이낸스 등)를 활용한 기능은 전용 앱을 활용하는 것이 편리하다 판단하여 구현하지 않을 계획입니다. ")


def setup(client):
    client.add_cog(Utils(client))
