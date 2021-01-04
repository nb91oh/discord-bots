import os
import re

import discord
from dotenv import load_dotenv

client = discord.Client()
load_dotenv()
discord_key = os.getenv('discord_key')
pattern = "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"



@client.event
async def on_message(message):
    if message.content.startswith('~scan'):
        messages = await message.channel.history(limit=1000000000).flatten()

        video_ids = []
        for message in messages:
            content = message.content
            link = re.search(pattern, content)
            if link:
                match = link.group(0)
                if "tu.be" in match:
                    video_id = match.split('/')[-1]
                    video_ids.append(video_id)
                else:
                    video_id = match.split('watch?v=')[-1]
                    video_ids.append(video_id)

        output = ",".join(video_ids)
        with open("video_ids.txt", "w+") as outfile:
            outfile.write(output)
        print("scan finished")

client.run(discord_key)