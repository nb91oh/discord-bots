import os
import time
import discord
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

client = discord.Client()
load_dotenv()
discord_key = os.getenv('image_search_key')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('~search'):
        search_terms = message.content.split('~search ')[-1].replace(' ', '+')
        url = "https://duckduckgo.com/?q={}&iar=images&iax=images&ia=images".format(search_terms)
        class_name = "tile--img__img"
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(10)
        element = driver.find_element_by_class_name(class_name)
        src = element.get_attribute('src')
        await message.channel.send(src)
        driver.close()

client.run(discord_key)

