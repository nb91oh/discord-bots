# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.update
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from dotenv import load_dotenv

load_dotenv()
playlist_id = os.getenv('youtube_playlist_id')

scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "yt_secrets.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

def insert(video_id):
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
    response = request.execute()

    print(response)

if __name__ == "__main__":
    with open("video_ids.txt") as f:
        video_ids = f.read().split(',')
    video_ids = video_ids[:199]
    for video_id in video_ids:
        try:
            insert(video_id)
        except:
            pass