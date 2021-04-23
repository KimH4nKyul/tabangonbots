# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
# import traceback
from random import choice
import requests
import asyncio
import time
import os
from json import loads

twitch_Client_ID = os.environ['twitchcid']
twitch_Client_secret = os.environ['twitchcsecret']
discord_Token = os.environ['token']
discord_channelID = os.environ['channel']
discord_bot_state = '티배깅 존나'
twitchID = 'tattoob0y'
# twitchID = 'screamdaddy93'
msg = ''

# client = discord.Client()
client = commands.Bot(command_prefix='!타봇 ', help_command=None)


@client.command(name='안녕')
async def hello(ctx):

    cmt = ["싸대기 탁! 야추 탁! 야꼭지 탁!", "응 싸대기 쳐맞어 그냥 쳐맞어 존나 쳐맞어"]

    await ctx.send(choice(cmt))


@client.event
async def on_ready():

    print(client.user.id)
    print("ready")

    # 디스코드 봇 상태 설정
    game = discord.Game(discord_bot_state)
    await client.change_presence(status=discord.Status.online, activity=game)

    # 채팅 채널 설정
    channel = client.get_channel(int(discord_channelID))
    await client.wait_until_ready()
    print(channel)

    # 트위치 api 2차인증
    oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twitch_Client_ID +
                              "&client_secret=" + twitch_Client_secret + "&grant_type=client_credentials")
    access_token = loads(oauth_key.text)["access_token"]
    token_type = 'Bearer '
    authorization = token_type + access_token
    print(authorization)

    check = False

    while client.is_ready:
        print("ready on Notification")
        headers = {'client-id': twitch_Client_ID,
                   'Authorization': authorization}

        response_channel = requests.get(
            'https://api.twitch.tv/helix/streams?user_login=' + twitchID, headers=headers)
        print("server: ", response_channel.text)

        try:
            if loads(response_channel.text)['data'][0]['type'] == 'live' and check == False:
                # await client.wait_until_ready()
                msg = time.strftime('%Y-%m-%d', time.localtime(
                    time.time())) + '\n타뱅온! 방송보러가기 : https://www.twitch.tv/' + twitchID
                await channel.send(msg)
                print("Online")
                check = True
        except:
            check = False
            # msg = '현재는 방송 중이 아닙니다! '
            # await channel.send(msg)
            # await client.wait_until_ready()
            print("Offline")
            # time.sleep(3600) # 1hours

        await asyncio.sleep(120)

client.run(discord_Token)
