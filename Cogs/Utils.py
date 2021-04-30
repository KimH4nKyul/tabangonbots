import os
from discord.ext import commands
import requests


class Utils(commands.Cog, name='유틸'):

    def __init__(self, client):
        self.client = client

    def concatText(self, v) -> str:

        text: str = ''
        for x in v:
            text = text + x + " "

        return text

    def serchIndex(self, v: str) -> str:

        my_lang = ['한국어', '영어', '중국어',
                   '대만어', '스페인어', '프랑스어', '베트남어', '태국어', '인도네시아어', '일본어']
        support_lang = ['ko', 'en', 'zh-CN',
                        'zh-TW', 'es', 'fr', 'vi', 'th', 'id', 'ja']

        res: str = ''
        if v in my_lang:
            res = support_lang[my_lang.index(v)]
        return res

    @commands.command(name="번역", help="", usage="!타봇 번역 <기준어> <번역어> <문장>")
    async def Translate(self, ctx, src, dst, *msg):

        papago_client_id = os.environ.get('papagoid')
        # papago_client_id = 'RVd7TKf_MwnlaBKg9zgq'
        papago_client_secret = os.environ.get('papagosecret')
        # papago_client_secret = ''

        text = self.concatText(msg)
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
            print(res.status_code)

        res.close()

    @commands.command(name='카카오맵', help="카카오맵으로 장소 검색하기", usage="!타봇 카카오맵 <주소 | 건물명>")
    async def KakaoMap(self, ctx, address):

        result = ""
        mAddress = self.concatText(address)
        # print(mAddress)

        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + mAddress
        # print(url)
        rest_api_key = '79bc4f11c9ddec8d8297ebb85d84d18f'
        header = {'Authorization': 'KakaoAK ' + rest_api_key}

        r = requests.get(url, headers=header)

        # print(r.status_code) # 200

        if r.status_code == 200:
            result_address = r.json()["documents"][0]["address"]

            result = result_address["y"], result_address["x"]
        else:
            result = "ERROR[" + str(r.status_code) + "]"

        print(mAddress+","+result[0]+","+result[1])
        # await ctx.send("https://map.kakao.com/link/map/"+mAddress+","+result[0]+","+result[1])

    @commands.command(name='코인', help="코인 관련 정보를 크롤링해 보여줘요. ", usage="!타봇 코인 <유튜브 | 뉴스>")
    async def Coin(self, ctx):

        await ctx.send("\n코인 기능은 유튜브 | 뉴스 정보만을 제공할 뿐 개인정보와 관련된 트레이딩 기능은 제공하지 않습니다. \n그외 OPEN API(업비트, 바이낸스 등)를 활용한 기능은 전용 앱을 활용하는 것이 편리하다 판단하여 구현하지 않을 계획입니다. ")


def setup(client):
    client.add_cog(Utils(client))
