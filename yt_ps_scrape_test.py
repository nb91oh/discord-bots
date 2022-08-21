import json
import os
import shutil
from yt_dlp import YoutubeDL


playlist_id = "PLYAQi7_zAOpYFACYGMYFdzHCXpYLmoU5C"
url = f"https://music.youtube.com/playlist?list={playlist_id}"

infodump = os.system(f'yt-dlp -J {url}')
print(infodump)

# if os.isdir(playlist_id):
#     shutil.rmtree(playlist_id)
# else:
#     os.mkdir(playlist_id)

# os.system(f'yt-dlp -x --audio-format "mp3" --audio-quality 0 -o "./{playlist_id}/%(title)s.%(ext)s" {url}')
