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

async def download_tiktok(url):
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = {"User-Agent": userAgent}) as response:
            long_url = response.url.human_repr()

    long_url = long_url.split('?')[0]
    print(long_url)
    user = long_url.split('/')[-3]
    video_id = long_url.split('/')[-1]

    share_url = f"https://www.tiktok.com/node/share/video/{user}/{video_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(share_url, headers = {"User-Agent": userAgent}) as response:
            data = await response.json()
            videoUrl = data["itemInfo"]["itemStruct"]["video"]["downloadAddr"]
            referer = data["seoProps"]["metaParams"]["canonicalHref"]
            print(videoUrl, referer)
        async with session.get(videoUrl, headers = {"Referer": referer, "User-Agent": userAgent}) as response:
            with open('video.mp4', 'wb') as f:
                video = await response.content.read()
                f.write(video)
    return True

async def download_tweet(url):
    url = 'https://' + url
    try:
        twittervideodl.download_video(url, "video")
    except Exception as e:
        print("no video found")
        print(e)
        return
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
        download = await download_tiktok(url)
    elif url_type == "twitter":
        print("downloading tweet...")
        download = await download_tweet(url)
        pass
    else:
        print("should not hit!!")
        return

    if download:
        async with message.channel.typing():
#            probe = ffmpeg.probe('video.mp4')
#            if int(probe['format']['size']) >= 8000000:
#                print("compressing video...")
#                await message.channel.send('compressing file...')
#                compress.compress()
            await message.channel.send(file = discord.File(fp = 'video.mp4'))
        print("sent a video")
    return

print("starting bot...")
client.run(discord_key)
