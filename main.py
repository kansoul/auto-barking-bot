import discord
import os
from dotenv import load_dotenv

client = discord.Client()

black_word = ['cc', 'đm', 'dm', 'địt mẹ', 'dit me', 'loz', 'con cac', 'con cặc', 'lồn']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  if message.author == client.user:
    return

  message_content = message.content.lower()
  for word in black_word:
    if word in message_content:
      await message.channel.send(f'Thằng <@{message.author.id}> Chửi thề con cặc. Đụ mẹ nói chuyện zô zăn hóa')
      return
  if 'alo' in message_content:
    await message.channel.send('@everyone alô alô. chơi game nào')
  if message_content == 'game':
    await message.channel.send('game nào')
  if message_content.startswith('chửi'):
    await message.channel.send(' '.join(message.content.split()[1:-1]).capitalize())
  if message_content in ('dit me quan', 'dm quan', 'địt mẹ quân', 'đm quân'):
    await message.channel.send('Ây ây. Điều quan trọng phải nhắc 3 lần chứ!')
    await message.channel.send(message)
    await message.channel.send(message)
    await message.channel.send(message)

load_dotenv()
client.run(os.getenv('TOKEN'))
