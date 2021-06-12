import discord
from discord import channel
from discord.ext import tasks
import cv2
import numpy as np
import requests
import urllib
import re
import textwrap
import feedparser
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
from datetime import datetime, timezone, timedelta
from time import mktime
import os
import glob
import random
from dotenv import load_dotenv


bot = discord.Client()

load_dotenv()

BOT_TOKEN = os.getenv('VNEXPRESS')
LIVING_ROOM = int(os.getenv('LIVING_ROOM'))

MARGIN = 20
IMAGE_WIDTH = 1000

def make_new(image, title, content, time):
    
    IMAGE_HEIGHT = int(IMAGE_WIDTH*image.shape[0]/image.shape[1])

    blank_image = np.ones((1000, 1000, 3), np.uint8)
    blank_image.fill(255)

    # Fill image
    image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
    blank_image[0:image.shape[0], 0:image.shape[1]] = image[:,:,:3]

    # Fill watermark
    logo = cv2.imread('vne_logo.png')
    logo = cv2.resize(logo, (100, 100))
    logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
    logo_size = logo.shape

    blank_image[20:20+logo_size[0], 20:20+logo_size[1]] = logo

    img_pil = Image.fromarray(blank_image)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype('./Merriweather-Regular.ttf', 32)
    offset = IMAGE_HEIGHT + 20

    for line in textwrap.wrap(title):
        draw.text(text=line, xy=(MARGIN, offset), font=font, fill='#9f224e')
        offset += font.getsize(line)[1]

    offset += 30

    for line in textwrap.wrap(content, width=58):
        draw.text((MARGIN, offset), line, font=font, fill="#000")
        offset += font.getsize(line)[1] + 5

    offset += 10


    draw.text((800, offset), time, font=ImageFont.truetype('./Merriweather-Regular.ttf', 24), fill="#333")

    return np.array(img_pil)

def clear_folder():
    files = glob.glob('news/*')
    for f in files:
        os.remove(f)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    content = message.content
    if content.startswith('!new '):
        num = content.split()[1]
        if num.isnumeric():
            num = int(num)
            if 0 < num < 6:
                xml_content = feedparser.parse('https://vnexpress.net/rss/tin-moi-nhat.rss')
                list = []
                for feed in xml_content.entries:
                    if len(list) == num:
                        break
                    title = feed.title
                    summary = BeautifulSoup(feed.summary, 'html.parser')
                    content = summary.find(text=True)
                    time = datetime.fromtimestamp(mktime(feed.published_parsed))
                    time += timedelta(hours=7)
                    time = time.strftime('%H:%M %d/%m/%y')

                    today = datetime.today().strftime('%y%m%d_%H%M%S')

                    img_tag = summary.findAll('img')
                    if img_tag:
                        url = img_tag[0]['src']
                        res = requests.get(url)
                        arr = np.asarray(bytearray(res.content), dtype=np.uint8)
                        try:
                            cover = cv2.cvtColor(cv2.imdecode(arr, -1), cv2.COLOR_BGRA2RGB)
                            cv2.imwrite('result.jpeg', cover)
                            image = make_new(cover, title, content, time)
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            filename = f'news/{today}_{random.randint(1000,9999)}.jpg'
                            list.append(filename)
                            cv2.imwrite(filename, image)
                        except Exception as e:
                            print('Error', e)
                        pass
                for f in list:
                    await message.channel.send(file=discord.File(f))
                clear_folder()
            else:
                await message.channel.send('đọc báo ít thôi')
        else:
            await message.channel.send('cmd ccjz')

@tasks.loop(seconds=1)
async def cron_job():
    await bot.wait_until_ready()
    channel = bot.get_channel(LIVING_ROOM)
    # Test room
    # channel = bot.get_channel(852466783213977623)
    today = datetime.today()
    # GMT+7
    today += timedelta(hours=7)
    date = today.strftime('%d/%m')
    h, m, s = today.hour, today.minute, today.second
    if h in (7, 12, 18) and m == 0 and s == 0:
        if h == 7:
            await channel.send(f'Bản tin sáng ngày {date}')
        elif h == 12:
            await channel.send(f'Bản tin trưa {date}')
        elif h == 18:
            await channel.send(f'Bản tin tối{date}')
        else:
            pass
        
        xml_content = feedparser.parse('https://vnexpress.net/rss/tin-moi-nhat.rss')
        list = []
        for feed in xml_content.entries:
            # Gen 5
            if len(list) == 5:
                break
            title = feed.title
            summary = BeautifulSoup(feed.summary, 'html.parser')
            content = summary.find(text=True)
            time = datetime.fromtimestamp(mktime(feed.published_parsed))
            time += timedelta(hours=7)
            time = time.strftime('%H:%M %d/%m/%y')

            today = datetime.today().strftime('%y%m%d_%H%M%S')

            img_tag = summary.findAll('img')
            if img_tag:
                url = img_tag[0]['src']
                res = requests.get(url)
                arr = np.asarray(bytearray(res.content), dtype=np.uint8)
                try:
                    cover = cv2.cvtColor(cv2.imdecode(arr, -1), cv2.COLOR_BGRA2RGB)
                    cv2.imwrite('result.jpeg', cover)
                    image = make_new(cover, title, content, time)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    filename = f'news/{today}_{random.randint(1000,9999)}.jpg'
                    list.append(filename)
                    cv2.imwrite(filename, image)
                except Exception as e:
                    print('Error', e)
            else:
                # print('No image found')
                pass
        for f in list:
            await channel.send(file=discord.File(f))
        clear_folder()

cron_job.start()
bot.run(BOT_TOKEN)