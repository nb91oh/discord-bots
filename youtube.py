import os
import re

import discord

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from dotenv import load_dotenv

client = discord.Client()
load_dotenv()
discord_key = os.getenv('discord_key')
playlist_id = os.getenv('youtube_playlist_id')
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "yt_secrets.json"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if str(message.channel) != 'groovy':
        return

    text = message.content
    pattern = "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
    link = re.search(pattern, text)
    if link:
        match = link.group(0)
        if "tu.be" in match:
            video_id = match.split('/')[-1]
        else:
            video_id = match.split('watch?v=')[-1]
    else:
        return

    request = youtube.playlistItems().insert(
        part = "snippet",
        body = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                    }
                }
            }
    )
    try:
        response = request.execute()
    except:
        await message.channel.send('link not added successfully :(')
    await message.channel.send("youtube link added to playlist!\nhttps://www.youtube.com/playlist?list=PLYAQi7_zAOpZgG3iXyhozqYo-B4DrnVco")

client.run(discord_key)