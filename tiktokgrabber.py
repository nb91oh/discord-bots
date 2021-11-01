#! /usr/bin/python3

import aiohttp
import os
import random
import re
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv


client = discord.Client()
load_dotenv()
discord_key = os.getenv('image_search_key')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    text = message.content
    pattern = "https:\/\/vm.tiktok.com/\w+"
    link = re.search(pattern, text)
    if link:
        url = link.group(0)
    else:
        return
    
    async with message.channel.typing():
        print(url)
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

            async with session.get(videoUrl, headers = {"Referer": referer, "User-Agent": userAgent}) as response:
                with open('tiktok.mp4', 'wb') as f:
                    video = await response.content.read()
                    f.write(video)

    await message.channel.send(file = discord.File(fp = 'tiktok.mp4'))




client.run(discord_key)
