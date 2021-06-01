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
    discord.File('images/tran_dan.jpg'),
    discord.File('trandan.mp4'),
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
    
    if message.author == client.user:
        return

    if message.channel.name == 'meme':
        global images
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                filename = f'meme/{time()}.jpeg'
                await attachment.save(filename)
                images.append(filename)
                num = random.randint(0, 10)
                if num < 1:
                    await message.channel.send(file=discord.File('images/kamui.jpeg'))
                return
    
    message_content = message.content.lower()
    words = message_content.split()

    # Special command

    if message_content == 'dlpl':
        await message.channel.send("!play https://www.youtube.com/playlist?list=PL8ZD0D4lXAriRazkWrqUo_3m0XiyqavuA")

    if message_content == 'meme':
        # global images

        if images == []:
            images = os.listdir('meme')
        
        random.shuffle(images)
        image = images.pop()
        
        await message.channel.send(file=discord.File(f'meme/{image}'))
    
    if message_content == "game":
        await message.channel.send("game nào")

    if 'lô' in words or "alo" in words or 'alô' in words:
        if random.randint(1, 10) % 2 == 0:
            await message.channel.send("@everyone alô alô. chơi game nào")
        else:
            await message.channel.send("lô cc")

    # Bad word
    if message_content in bad_word:
        await message.channel.send(random.choice(bad_word_response))

    



load_dotenv()
client.run(os.getenv("TOKEN"))
