#! /usr/bin/python3

import os
import time
import discord
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        src = element.get_attribute('src')
        await message.channel.send(src)
        driver.close()

client.run(discord_key)

