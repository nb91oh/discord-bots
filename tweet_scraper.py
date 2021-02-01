import os
import re
import psycopg2
import discord
from dotenv import load_dotenv

client = discord.Client()
load_dotenv()
discord_key = os.getenv('discord_key')
pg_user = os.getenv('PG_USER')
pg_pass = os.getenv('PG_PASS')
pg_port = os.getenv('PG_PORT')
pg_host = os.getenv('PG_HOST')
pg_db = os.getenv('PG_DB')
pattern = "twitter.com\/\D+\/status\/\d+"

@client.event
async def on_message(message):
    # if message.content.startswith('~scan'):
    #     print('scan started')
    #     messages = await message.channel.history(limit=100000000000).flatten()
    #     twitter_urls = []
    #     for message in messages:
    #         content = message.content
    #         link = re.search(pattern, content)
    #         if link:
    #             match = 'https://' + link.group(0)
    #             twitter_urls.append(match)
    #     conn = psycopg2.connect(dbname = pg_db, host = pg_host, port = pg_port, user = pg_user, password = pg_pass)
    #     cur = conn.cursor()
    #     cur.execute('DELETE FROM urls')
    #     for twitter_url in twitter_urls:
    #         cur.execute('INSERT INTO urls (url) VALUES (%s)', (twitter_url,))
    #     conn.commit()
    #     conn.close()
    #     print("scan finished")
    if message.channel.id != 491361907521880095:
        return
    link = re.search(pattern, message.content)
    if link:
        match = 'https://' + link.group(0)
        conn = psycopg2.connect(dbname = pg_db, host = pg_host, port = pg_port, user = pg_user, password = pg_pass)
        cur = conn.cursor()
        cur.execute('INSERT INTO urls (url) VALUES (%s)', (str(match),))
        conn.commit()
        conn.close()

client.run(discord_key)