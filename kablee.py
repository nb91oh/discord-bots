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
import twittervideodl


client = discord.Client()
load_dotenv()
discord_key = os.getenv('image_search_key')


async def download(url):
    os.system(f'youtube-dl --output \"video.mp4\" {url}')
    return True

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    text = message.content
    regex_lookup = {
        "tiktok": "https:\/\/vm.tiktok.com/\w+",
        "twitter": "twitter.com\/\D+\/status\/\d+"
    }
    url = None
    for platform, pattern in regex_lookup.items():
        link = re.search(pattern, text)
        if link:
            url_type = platform
            url = link.group(0)
            break
    if not url:
        return
    print("url found:" + url)
    if url_type == "tiktok":
        print("downloading tiktok...")
        # download = await download_tiktok(url)
        dl = await download(url)
    elif url_type == "twitter":
        print("downloading tweet...")
        # download = await download_tweet(url)
        dl = await download(url)
        pass
    else:
        print("should not hit!!")
        return

    if dl:
        async with message.channel.typing():
            # discord has 8mb file limit
            # want to compress with ffmpeg but cant do math good

#            probe = ffmpeg.probe('video.mp4')
#            if int(probe['format']['size']) >= 8000000:
#                print("compressing video...")
#                await message.channel.send('compressing file...')
#                compress.compress()
            await message.channel.send(file = discord.File(fp = 'video.mp4'))
        print("sent a video")
        os.remove("video.mp4")
    return

print("starting bot...")
client.run(discord_key)
