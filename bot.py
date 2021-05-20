# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
# import traceback
import requests
import asyncio
import time
import os
from json import loads

twitch_Client_ID = os.environ.get('twitchid')
twitch_Client_secret = os.environ.get('twitchsecret')
discord_Token = os.environ.get('token')
discord_channelID = os.environ.get('channel')
discord_bot_state = ''
twitchID = 'tattoob0y'
# twitchID = 'hanseoryeong'
msg = ''

client = commands.Bot(command_prefix='!타봇 ', help_command=None)

try:
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            client.load_extension(f'Cogs.{filename[:-3]}')
except Exception as e:
    fmt = f"{type(e).__name__}: {e}"
    print("\nReload Error: \n", fmt)


@client.command(name="리로드")
async def reload_commands(ctx, extension=None):
    if extension is None:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                try:
                    client.unload_extension(f"Cogs.{filename[:-3]}")
                    client.load_extension(f"Cogs.{filename[:-3]}")
                    await ctx.send(f":white_check_mark: {filename[:-3]} 명령어를 다시 불러왔습니다.")
                except Exception as e:
                    fmt = f"{type(e).__name__}: {e}"
                    print("\nReload Error: \n", fmt)
    else:
        try:
            client.unload_extension(f"Cogs.{extension}")
            client.load_extension(f"Cogs.{extension}")
            await ctx.send(f":white_check_mark: {extension}을(를) 다시 불러왔습니다.")
        except Exception as e:
            fmt = f"{type(e).__name__}: {e}"
            print("\nReload Error: \n", fmt)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("그런 명령어는 없습니다. ")
        # return
    elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await ctx.send("명령어 인자가 부족합니다. ")
    else:
        embed = discord.Embed(
            title="Error", description="Reporting error", color=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        await ctx.send("잘못된 명령어 사용법입니다. \n", embed=embed)


@client.event
async def on_ready():

    print("ready: \n", client.user.name, client.user.id)

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

    # while client.is_ready:
    while True:
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
                    time.time())) + '\n타뱅온! 방송보러가기 : https://www.twitch.tv/' + 'dogswellfish'
                await channel.send("\n 테스트 메시지 입니다. ")
                print("Online")
                check = True
        except:
            check = False
            # msg = '현재는 방송 중이 아닙니다! '
            # await channel.send(msg)
            # await client.wait_until_ready()
            print("Offline")
            # time.sleep(3600) # 1hours

        await asyncio.sleep(30)

client.run(discord_Token)
