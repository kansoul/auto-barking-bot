import discord
import requests
from time import time
import os
from dotenv import load_dotenv
import random

client = discord.Client()

image_types = ["png", "jpeg", "gif", "jpg"]

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
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save(f'meme/{time()}.jpeg')
                return
    
    message_content = message.content.lower()
    words = message_content.split()

    # Special command

    if message_content == 'dlpl':
        await message.channel.send("!play https://www.youtube.com/playlist?list=PL8ZD0D4lXAriRazkWrqUo_3m0XiyqavuA")

    if message_content == 'meme':
        images = os.listdir('meme')
        image = random.choice(images)
        await message.channel.send(file=discord.File(f'meme/{image}'))

    if words[0] == '!show' and len(words) > 1:
        url = words[1]
        image_content = requests.get(url).content
        with open(f'meme/{int(time())}.jpeg', 'wb') as f:
            f.write(image_content)
        await message.channel.send(file=discord.File(image_content))


    if "alo" in words or 'alô' in words:
        await message.channel.send("@everyone alô alô. chơi game nào")
    
    if message_content == "game":
        await message.channel.send("game nào")

    if message_content.startswith("chửi"):
        if words[-1] == 'đi':
            await message.channel.send(" ".join(message.content.split()[1:-1]).capitalize())
        else:
            await message.channel.send(" ".join(message.content.split()[1:]).capitalize())

    # Load content
    with open('content.txt', encoding='utf-8') as f:
        for row in f.readlines():
            row = parse_row(row.strip().split(','))

            if row['condition'] == 1 and row['content'] == message_content:
                if row['reply_content'] != '':
                    await message.channel.send(row['reply_content'])
                if row['image'] != '':
                    await message.channel.send(file=discord.File(f'images/{row["image"]}'))
            elif row['condition'] == 0:
                if row['content'].count(' ') == 0 and row['content'] in words:
                    if row['reply_content'] != '':
                        await message.channel.send(row['reply_content'])
                    if row['image'] != '':
                        await message.channel.send(file=discord.File(f'images/{row["image"]}'))
                else:
                    if row['content'] in message_content:
                        if row['reply_content'] != '':
                            await message.channel.send(row['reply_content'])
                        if row['image'] != '':
                            await message.channel.send(file=discord.File(f'images/{row["image"]}'))



load_dotenv()
client.run(os.getenv("TOKEN"))
