#! /usr/bin/python
import aiohttp
import os
import re
import sys
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
import ffmpeg
import compress


client = discord.Client()
load_dotenv()
discord_key = os.getenv('image_search_key')


async def download(url):
    if os.path.exists('video.mp4'):
        os.remove("video.mp4")
    os.system(f'youtube-dl --output \"video.mp4\" {url}')
    if os.path.exists('video.mp4'):
        print("video downloaded")
        return True
    else:
        print("error downloading")
        return False

async def send(message):
    await message.channel.send(file = discord.File(fp = 'video.mp4'))
    print("sent a video")
    os.remove("video.mp4")
    return


async def check_message(message):
    text = message.content
    regex_lookup = {
        "tiktok": "https:\/\/vm.tiktok.com/\w+",
        "twitter": "twitter.com\/\D+\/status\/\d+",
        "reddit": "https:\/\/www.reddit.com\/r\/\w+\/\w+\/\w+\/\w+"
    }
    url = None
    for platform, pattern in regex_lookup.items():
        link = re.search(pattern, text)
        if link:
            url_type = platform
            url = link.group(0)
            break
    if not url:
        return False
    else:
        print(f"url found: {url}")
        return url


async def compress_video():
    pass


async def check_video():
    probe = ffmpeg.probe('video.mp4')
    if int(probe['format']['size']) > 8388608:
        return False
    return True


@client.event
async def on_reaction_add(reaction, user):
    print(str(reaction))
    if str(reaction) == "<:save:1006915822352093315>":
        print("save requested")
        url = await check_message(reaction.message)
        if not url:
            print("no url in message")
            return
        dl = await download(url)
        if not dl:
            await reaction.message.channel.send("error downloading...")
            return
        if not await check_video():
            await reaction.message.channel.send("compressing video...")
            # compress_video()
            return
        await send(reaction.message)
        return 
    else:
        return



print("starting bot...")
client.run(discord_key)
