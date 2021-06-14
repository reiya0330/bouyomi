import discord
from discord.ext import commands
import asyncio
import os
import subprocess
import ffmpeg
from voice_generator import creat_WAV

client = commands.Bot(command_prefix='.')
voice_client = None

server_id_test = 853623328849264692
text_id_test = 853623328849264695
voice_id_test = 853623329306705940
    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command()
async def join(ctx):
    print('#join')
    print('#voicechannelを取得')
    vc = ctx.author.voice.channel
    print('#voicechannelに接続')
    await vc.connect()

@client.command()
async def bye(ctx):
    print('#bye')
    print('#切断')
    await ctx.voice_client.disconnect()

@client.command()
async def register(ctx, arg1, arg2):
    with open('C:/open_jtalk/bin/dic.txt', mode='a') as f:
        f.write('\n'+ arg1 + ',' + arg2)
        print('dic.txtに書き込み：''\n'+ arg1 + ',' + arg2)
    await ctx.send('`' + arg1+'` を `'+arg2+'` として登録しました')

@client.event
async def on_voice_state_update(member, before, after):

    if before.channel != after.channel:
        if after.channel is not None:            
            for channel in member.guild.voice_channels:
                if channel.id == voice_id_test and len(channel.members) == 1:
                    vc = member.voice.channel
                    await vc.connect()
        
        if before.channel is not None :
            for channel in member.guild.voice_channels:
                if channel.id == voice_id_test and len(channel.members) == 1 and channel.members[0].name=='棒読みちゃん':              
                    await member.guild.voice_client.disconnect()
            
            
    if member.guild.id == server_id_test:   # サーバーid
        text_ch = client.get_channel(text_id_test)   # 通知させたいTEXTチャンネルid
        if before.channel is None:
            if member.nick is not None:
                msg = f'{member.nick}さんが参加しました。'
                await text_ch.send(msg)
            elif not member.bot:
                msg = f'{member.name}さんが参加しました。'
                await text_ch.send(msg)
                
    if member.guild.id == server_id_test:   # サーバーid
        text_ch = client.get_channel(text_id_test)   # 通知させたいTEXTチャンネルid
        if after.channel is None:
            if member.nick is not None:
                msg = f'{member.nick}さんが退出しました。'
                await text_ch.send(msg)
            elif not member.bot:
                msg = f'{member.name}さんが退出しました。'
                await text_ch.send(msg)                

@client.event
async def on_message(message):
    print('---on_message_start---')
    msgclient = message.guild.voice_client
    print(msgclient)
    if message.content.startswith('.'):
        pass

    else:
        if message.guild.voice_client:
            print('Nick=' + str(message.author.nick))
            if message.author.nick is not None:
                message.content = message.author.nick + 'さん曰く、' + message.content
                
            else:
                if message.author.name != '棒読みちゃん':
                    message.content = message.author.name + 'さん曰く、' + message.content
                
           
            creat_WAV(message.content)
            source = discord.FFmpegPCMAudio("output.wav")
            message.guild.voice_client.play(source)                         
        else:
            pass
    await client.process_commands(message)
    print('---on_message_end---')


client.run("ODUzNjIxOTA2MjQ1OTQzMzA2.YMYDWQ.5J56tyiOjEmuupOJLMcAgaDWBrs")
