#! /usr/bin/python
import datetime
import os
import re
import sys
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
import ffmpeg
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtube_search import YoutubeSearch
import compress


client = discord.Client()
load_dotenv()
discord_key = os.getenv('image_search_key')

scope = 'playlist-read-private'

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
redirect_uri = os.getenv('redirect_uri')
username = os.getenv('username')
playlist_id = os.getenv('playlist_id')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=redirect_uri,
    username=username))


async def download(url):
    if os.path.exists('video.mp4'):
        os.remove("video.mp4")
    os.system(f'yt-dlp -S "vcodec:h264" --output \"video.mp4\" {url}')
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


async def check_playlist_link(content):
    regex_lookup = {
        "spotify": "https:\/\/open.spotify.com\/playlist\/\w+",
        "youtube": "https:\/\/music.youtube.com/playlist\?list=\w+",
    }
    for platform, pattern in regex_lookup.items():
        link = re.search(pattern, content)
        if link:
            url = link.group(0)
            if platform == "spotify":
                playlist_id = url.split("/")[-1]
            elif platform == "youtube":
                playlist_id = url.split("=")[-1]
            print(playlist_id)
            return platform, playlist_id
        else:
            return False


async def scrape_data(platform, playlist_id):
    if platform == "spotify":
        try:
            playlist = sp.playlist_items(playlist_id)
        except:
            print("failed to call sp.playlist_items()")
            return
        playlist_data = []
        for song in playlist['items']:
            artist = song['track']['artists'][0]['name']
            song_name = song['track']['name']
            track = {"artist": artist, "name": song_name}
            playlist_data.append(track)
        return playlist_data
    elif platform == "youtube":
        pass
    

async def gather_youtube(playlist_data):
    yt_playlist = []
    confirm_text = ""
    for track_no, track in enumerate(playlist_data):
        artist = track['artist']
        name = track['name']
        results = YoutubeSearch(f'{artist}  {name}', max_results=1).to_dict()
        yt_url = "youtube.com/" + results[0]['url_suffix']
        yt_title = results[0]['title']
        yt_track_info = {"yt_title": yt_title, "yt_url": yt_url}
        confirm_text += f"#{track_no + 1} -- {yt_title}\n"
        yt_playlist.append(yt_track_info)
    with open("playlist.txt", "w") as f:
        print(yt_playlist, file=f)
    return confirm_text


async def dl_playlist(reaction, user):
    platform, playlist_id = await check_playlist_link(reaction.message.content)
    if not playlist_id:
        return
    playlist_data = await scrape_data(platform, playlist_id)
    confirm_text = await gather_youtube(playlist_data)
    await reaction.message.channel.send(f"Check the below playlist...\n\n{confirm_text}")


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
    elif str(reaction).split(":")[1] == "burn":
            await dl_playlist(reaction, user)
    else:
        return



print("starting bot...")
client.run(discord_key)
