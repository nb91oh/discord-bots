import discord
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

client = discord.Client()

load_dotenv()


client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv('redirect_uri')
username = os.getenv('username')
playlist_id = os.getenv('playlist_id')
discord_key = os.getenv('discord_key')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public', 
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=redirect_uri,
    username=username))

@client.event
async def on_message(message):
    url = 'https://open.spotify.com/track/'
    if message.content.startswith(url):
        track_id = message.content.split('/')[-1]
        tracks = [track_id]

        sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=tracks)

        await message.channel.send(f'https://open.spotify.com/playlist/{playlist_id}')



client.run(discord_key)
