import discord
from discord import channel
import requests
from time import time
import os
from dotenv import load_dotenv
import random

client = discord.Client()

image_types = ["png", "jpeg", "gif", "jpg"]
images = os.listdir('meme')

bad_word = ['cc', 'đm', 'dm', 'loz', 'lồn', 'ditmequan', 'cl']

bad_word_response = [
    'chửi con cặc. mày nói chuyện gì mà tục tĩu quá vậy mày',
    'thằng zô zăn hóa. con chó của cộng sản',
    'chửi thề con cặc. đụ mẹ nói chuyện zô zăn hóa',
    '|images/tran_dan.jpg',
    '|trandan.mp4',
]

def parse_row(row):
    return {
        'content': row[0],
        'condition': int(row[1]),
        'reply_type': int(row[2]),
        'reply_content': row[3],
        'image': row[4],
        'mention_everyone': int(row[5])
    }

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global images


    if message.author == client.user:
        return
    
    message_content = message.content.lower()
    words = message_content.split()

    # Special command

    if message_content == 'dlpl':
        await message.channel.send("!play https://www.youtube.com/playlist?list=PL8ZD0D4lXAriRazkWrqUo_3m0XiyqavuA")

    if message_content == 'meme':
        await message.channel.send('Không lưu meme nữa. Nặng quá!')
    
    if message_content == "game":
        if random.randint(1, 10) == 0:
            await message.channel.send("game nào")
        else:
            await message.channel.send("nghiện")

    if 'lô' in words or "alo" in words or 'alô' in words:
        messages = [['@everyone alô alô. chơi game nào'],\
                    ['lô cc'], ['lại tính rủ chơi gêm chứ gì. t hiểu tụi mày quá', 'để t rủ cho', '@everyone gem nào các giáo sư'], \
                        ['lô cc gì mà lô']]
        l = random.choice(messages)
        for m in l:
            await message.channel.send(m)

    # Bad word
    if message_content in bad_word:
        temp = random.choice(bad_word_response)
        if temp[0] == '|':
            await message.channel.send(file=discord.File(temp[1:]))
        else:
            await message.channel.send(temp)

    



load_dotenv()
client.run(os.getenv("TOKEN"))
