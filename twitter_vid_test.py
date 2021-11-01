#! /usr/bin/python3

import aiohttp
import os
import random
import re
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
import twittervideodl


client = discord.Client()
load_dotenv()
discord_key = os.getenv('image_search_key')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    text = message.content
    pattern = "twitter.com\/\D+\/status\/\d+"
    link = re.search(pattern, text)
    if link:
        url = 'https://' + link.group(0)
    else:
        return
    embeds = message.embeds
    if 'video' not in embeds[0].to_dict().keys():
        return
    twittervideodl.download_video(url, "tweet")    
    await message.channel.send(file = discord.File(fp = "tweet.mp4"))



client.run(discord_key)
