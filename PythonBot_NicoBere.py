#Zantes Bot created by Nico Bere, Germany
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import random
from random import randint
import logging
import safygiphy
import requests
import lxml
from lxml.html import fromstring
import pyglet
import io
import os
from itertools import cycle
import praw
import ffmpy
from ffmpy import FFmpeg
import asyncore
import asyncio
import time
from weather import Weather, Unit
from googletrans import Translator

bot = commands.Bot(command_prefix='#')
bot.remove_command("help")
token = "My bot token is a secrete ;)"
client = discord.Client()
sgif = safygiphy.Giphy()
reddit_praw = praw.Reddit(client_id="secret", client_secret="secret" ,username="secret", password="secret", user_agent="secret")
reddid_icon = "http://icons.iconarchive.com/icons/papirus-team/papirus-apps/128/reddit-icon.png"


ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}
translator = Translator(service_urls=[
      'translate.google.com',
])

#Colors Fail = Red | Success = Green | Fluffy = Orange
fail_col = 0xF90006
success_col = 0x00F92C
fluffy_col = 0xe4af01

#----------------------------------- Start ------------------------------------
@bot.event
async def on_ready():
    print("Ready to start")
    print("This is a Bot for " + bot.user.name)
    print("With the ID: "+ bot.user.id)
    await bot.change_presence(game=discord.Game(name="Online"))
#------------------------------------------------------------------------------


# Changing the Bot presence
@bot.command(pass_context=True)
async def botgame(ctx, args):
    print("{} has executed the command 'botgame'".format(ctx.message.author.name))
    await bot.change_presence(game=discord.Game(name=args))
    await bot.say("My presence was set to: ``{}``".format(args))
    await bot.delete_message(ctx.message)


# Translating a text into another chosen language
@bot.command(pass_context=True)
async def trans(ctx, transtext, lang):
    print("{} has executed the command 'trans'".format(ctx.message.author.name))
    
    # For easier chinese-language translation
    if lang == "cn":
        lang = "zh-CN"

    translations = translator.translate([transtext], dest=lang)
    for translation in translations:
        print(translation.origin, " -> ", translation.text)
        await bot.say(translation.text)


# Gives you a random ranged value between 1 and your given number 
@bot.command(pass_context=True)
async def rand(ctx, val: int):
    print("{} has executed the command 'rand'".format(ctx.message.author.name) + " and value {}".format(val))
    
    try:
        rnd = random.randint(1, val)
        embed = discord.Embed(color=fluffy_col)
        embed.add_field(name="Random", value="Result: " + str(rnd), inline=True)
    except ValueError:
        embed = discord.Embed(color=fluffy_col)
        embed.add_field(name="Failed", value="Must be a HIGHER number than ZERO or LESS", inline=True)

    await bot.say(embed=embed)


# Shows all possible commands the BOT can use
@bot.command(pass_context=True)
async def help(ctx):
    print("{} has executed the command 'help'".format(ctx.message.author.name))

    embed = discord.Embed(title="Commands", color=fluffy_col)
    embed.add_field(name=":wrench: All Commands are Linked :wrench: ", value="#help", inline=True)
    await bot.say(embed=embed)


# Gives you information about the member
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    print("{} has executed the command 'info'".format(ctx.message.author.name))
    
    embed = discord.Embed(title="Information {}".format(user.name) , color=fluffy_col)
    embed.add_field(name="Name: ", value=user.name, inline=True)
    embed.add_field(name="ID: ", value=user.id, inline=True)
    embed.add_field(name="Status: ", value=user.status, inline=True)
    embed.add_field(name="Top Role: ", value=user.top_role, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    
    await bot.say(embed=embed)
    

# Example of the Avatar the member is using
@bot.command(pass_context=True)
async def avatar(ctx, user: discord.Member):
    print("{} has executed the command 'avatar'".format(ctx.message.author.name))

    embed = discord.Embed(color=fluffy_col)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)


# GIF will be sent to textchannel by searching for a tag or by random
@bot.command(pass_context=True)
async def gif(ctx, gifname: None):
    if gifname is None:
        print("{} has executed the command 'gif' ".format(ctx.message.author.name))
    else:
        print("{} has executed the command 'gif' ".format(ctx.message.author.name) + " with tag {}".format(gifname))

    try:
        if gifname is None:
            rgif = sgif.random()
        else:
            rgif = sgif.random(tag=str(gifname))
            
        response = requests.get(str(rgif.get("data", {}).get("image_original_url")), stream=True)
        await bot.send_file(ctx.message.channel , io.BytesIO(response.raw.read()), filename="video.gif")
    
    except AttributeError:
        print("AttributeError occured on command 'gif'")
        

# Subreddit Image will be sent to textchannel by searching for a tag or by random
@bot.command(pass_context=True)
async def reddit(ctx, tag):
    print("{} has executed the command 'reddit'".format(ctx.message.author.name) + " with tag {}".format(tag))

    embed = discord.Embed(color=fluffy_col)
    submissions = reddit_praw.subreddit(tag).hot(limit=5)
    
    for item in submissions:
        embed.set_author(name=item.title, url=item.url, icon_url=reddid_icon)
        embed.set_image(url=item.url)
        embed.set_footer(text="👍 {}".format(item.ups) + " | 💬 {}".format(item.num_comments), icon_url=ctx.message.author.avatar_url)

    await bot.say(embed=embed)


# MEME will be sent to textchannel by searching for a tag or by random
@bot.command(pass_context=True)
async def meme(ctx):
    print("{} has executed the command 'meme'".format(ctx.message.author.name))

    embed = discord.Embed(color=fluffy_col)
    rnd = random.randint(1, 200)
    submissions = reddit_praw.subreddit("DeepFriedMemes").hot(limit=rnd)
    
    for item in submissions:
        embed.set_author(name=item.title, url=item.url, icon_url=reddid_icon)
        embed.set_image(url=item.url)
        embed.set_footer(text="👍 {}".format(item.ups) + " | 💬 {}".format(item.num_comments), icon_url=ctx.message.author.avatar_url)
    
    await bot.say(embed=embed)


# Post a bird picture from reddit
@bot.command(pass_context=True)
async def birb(ctx):
    print("{} has executed the command 'birb'".format(ctx.message.author.name))

    embed = discord.Embed(color=fluffy_col)
    rnd = random.randint(1, 200)
    submissions = reddit_praw.subreddit("birb").hot(limit=rnd)
    
    for item in submissions:
        embed.set_author(name=item.title, url=item.url, icon_url=reddid_icon)
        embed.set_image(url=item.url)

    await bot.say(embed=embed)


# Kick a person on the Server
@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    print("{} has executed the command 'kick'".format(ctx.message.author.name))

    await bot.say(":boom: User '{}' got kicked from the server :boom:".format(user.name))
    await bot.kick(user)
    

# Ban a person on the Server
@bot.command(pass_context=True)
async def ban(ctx, user: discord.Member):
    print("{} has executed the command 'ban'".format(ctx.message.author.name))

    await bot.say(":boom: User '{}' got banned from the server :boom:".format(user.name))
    await bot.ban(user)


# Unban a person on the Server
@bot.command(pass_context=True)
async def unban(ctx):
    print("{} has executed the command 'unban'".format(ctx.message.author.name))
    
    ban_list = await bot.get_bans(ctx.message.server)
    
    await bot.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))
    
    if not ban_list:
        await bot.say("Ban list is empty")
    try:
        await bot.unban(ctx.message.server, ban_list[-1])
        await bot.say("Unbanned user: `{}`".format(ban_list[-1].name))
    except discord.HTTPException:
        await bot.say("Unban failed")
    

# Playing TBH MP3's (TBH Playlist only exist on my Personal Computer ,its only for privat usage)
@bot.command(pass_context=True)
async def TBH(ctx, val):
    print("{} has executed the command 'TBH'".format(ctx.message.author.name) + " and value {}".format(val))
    
    if ctx.message.server.voice_client is None:
        voice = await bot.join_voice_channel(ctx.message.author.voice_channel)
    elif ctx.message.server.voice_client is not None:
        voice = ctx.message.server.voice_client

    player = voice.create_ffmpeg_player("R:/randompath1/randompath2/{}.mp3".format(val)) # Just a Path Filler
    await bot.delete_message(ctx.message)
    player.start()


# Weather API
@bot.command(pass_context=True)
async def weather(ctx, loc):
    print("{} has executed the command 'weather'".format(ctx.message.author.name))

    await bot.delete_message(ctx.message)
    m_weather = Weather(unit=Unit.CELSIUS)
    location = m_weather.lookup_by_location(loc)
    forecasts = location.forecast
    condition = location.condition
    ct = condition.text

    await bot.say("---------------------------------------------")
    await bot.say("Weather for " + loc)
    await bot.say("Today's condition: {}".format(ct))
    await bot.say("---------------------------------------------")

    for forecast in forecasts:
        weekday = forecast.date
        await bot.say("({}) ".format(weekday) + "🌞: " + forecast.high + "°C | 🌙: " + forecast.low + "°C")


# Playing Soundboard TS MP3's (TS Playlist only exist on my Personal Computer ,its only for privat usage)
@bot.command(pass_context=True)
async def ts(ctx, val):
    print("{} has executed the command 'ts'".format(ctx.message.author.name) + " and value {}".format(val))
    
    if ctx.message.server.voice_client is None:
        voice = await bot.join_voice_channel(ctx.message.author.voice_channel)
        player = voice.create_ffmpeg_player("R:/randompath1/randompath2/random.mp3") # Just a Path Filler
        player.start()
        time.sleep(4.5)
    elif ctx.message.server.voice_client is not None:
        voice = ctx.message.server.voice_client


    player = voice.create_ffmpeg_player("R:/randompath1/randompath2/{}.mp3".format(val)) # Just a Path Filler
    await bot.delete_message(ctx.message)
    player.start()


# Playing Soundboard DL MP3's (DL Playlist only exist on my Personal Computer ,its only for privat usage)
@bot.command(pass_context=True)
async def dl(ctx, val):
    print("{} has executed the command 'dl'".format(ctx.message.author.name) + " and value {}".format(val))
    
    if ctx.message.server.voice_client is None:
        voice = await bot.join_voice_channel(ctx.message.author.voice_channel)
    elif ctx.message.server.voice_client is not None:
        voice = ctx.message.server.voice_client

    player = voice.create_ffmpeg_player("R:/randompath1/randompath2/{}.mp3".format(val)) # Just a Path Filler
    await bot.delete_message(ctx.message)
    player.start()


# Move an user to your VoiceChannel
@bot.command(pass_context=True)
async def move(ctx, member: discord.Member):
    print("{} has executed the command 'move'".format(ctx.message.author.name))
    vc = ctx.message.author.voice_channel
    
    if member.voice_channel.name == vc.name:
        embed = discord.Embed(color=fail_col)
        embed.add_field(name="Failed", value="Member **{}**".format(member.name) + " is already in this Voice Channel")
    else:
        embed = discord.Embed(color=success_col)
        await bot.move_member(member, vc)
        embed.add_field(name="Moved", value="**{}**".format(member.name) + " got moved to " + "`{}`".format(vc.name) + " by **{}**".format(ctx.message.author.name), inline=True)
    await bot.say(embed=embed)
    await bot.delete_message(ctx.message)


# Move an user to your VoiceChannel
@bot.command(pass_context=True)
async def user(ctx):
    print("{} has executed the command 'user'".format(ctx.message.author.name))
    server_members = ctx.message.server.members
    author_channel = ctx.message.author.voice_channel
    count = 0
    # Get all server members
    for member in server_members:
        member_channel = member.voice_channel
        count += 1
        if member_channel is not False and member_channel is author_channel:
            embed = discord.Embed(color=fluffy_col)
            embed.add_field(name="User {}".format(count), value=member.name, inline=True)
            await bot.say(embed=embed)

 
# Shows which game you are currently playing
@bot.command(pass_context=True)
async def game(ctx, member: discord.Member = None):
    print("{} has executed the command 'game'".format(ctx.message.author.name))
    
    # Self
    if member is None and ctx.message.author.game is not None:
        await bot.say("You're playing: ``" + str(ctx.message.author.game) + "``")
    elif member is None and ctx.message.author.game is None:
        await bot.say("You're playing ``Nothing``")
        
    # Members
    if member is not None and member.game is not None:
        await bot.say("{} is playing: ``".format(member.name) + str(member.game) + "``")
    elif member is not None and member.game is None:
        await bot.say("{} is playing ``Nothing``".format(member.name))


# Change the Nickname of an member
@bot.command(pass_context=True)
async def nick(ctx, member: discord.Member, _nick: str,):
    print("{} has executed the command 'nick'".format(ctx.message.author.name))

    await bot.change_nickname(member, _nick)
    await bot.delete_message(ctx.message)


# Join / Let Bot join your voice channel
@bot.command(pass_context=True)
async def join(ctx):
    author = ctx.message.author
    channel = ctx.message.author.voice_channel
    print("{} has executed the command 'join'".format(author.name))

    if channel is None:
        embed = discord.Embed(color=fail_col)
        embed.add_field(name="Failed", value="I only can join if you are in a valid Voice Channel", inline=True)
    else:
        embed = discord.Embed(color=success_col)
        embed.add_field(name="Im Here!", value="Joining Channel " + channel.name, inline=True)
        await bot.join_voice_channel(channel)
    await bot.say(embed=embed)
        

# Disconnect, Dc / Let Bot disconnect from your voice channel
@bot.command(pass_context=True, no_pm=True)
async def dc(ctx):
    print("{} has executed the command 'dc'".format(ctx.message.author.name))
    
    for x in bot.voice_clients:
        if(x.server is ctx.message.server):
            await bot.say("Im about to disconnect.")
            await x.disconnect()


# Runs the Bot Client with the given unique token
bot.run(token)