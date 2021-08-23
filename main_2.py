import discord
from discord import Embed
import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import random
import matplotlib.pyplot as plt

client = discord.Client()

image_types = ["png", "jpeg", "gif", "jpg"]
images = os.listdir('meme')

bad_word = ['cc', 'đm', 'dm', 'loz', 'lồn', 'ditme', 'cl', 'cẹk']

bad_word_response = [
    'chửi con cặc. mày nói chuyện gì mà tục tĩu quá vậy mày',
    'thằng zô zăn hóa. con chó của cộng sản',
    'chửi thề con cặc. đụ mẹ nói chuyện zô zăn hóa',
    '|images/tran_dan.jpg',
    '|trandan.mp4',
]

API_URL = 'https://api.apify.com/v2/key-value-stores/ZsOpZgeg7dFS1rgfM/records/LATEST'

id_dict = {
    '835374442577526785': 'me',
    '682229605092163584': ['Ditmequan'],
    '452524506578288681': ['Sủa cc j vậy thằng fake'],
    '486145075706069004': ['Đức Anh Dz']
}

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global images

    if message.author == client.user:
        return

    author = str(message.author.id)
    
    message_content = message.content.lower()
    words = message_content.split()

    # Special command
    if message_content in ('covid', 'covid-19', 'covid 19', 'corona'):
        res = requests.get(API_URL)
        data = res.json()
        embed = Embed()
        embed.set_author(name='Bộ Y Tế', url=data['sourceUrl'], icon_url='https://vitratecom.vn/wp-content/uploads/2019/08/2018-08-13-011414.6356512018-01-11-110703.688533boyte.png')
        embed.set_thumbnail(url='https://www.uia.no/var/uia/storage/images/media/images/2020-nyhetsbilder-2-hoest/korona-viruset-2871-cdc-alissa-eckert-ms_modifisert-970/1945937-1-nor-NO/korona-viruset-2871-cdc-alissa-eckert-ms_modifisert-970_fullwidth.jpg')
        embed.title = 'Tình hình Covid tại Việt Nam'
        embed.add_field(name='Số ca', value=f'{data["infected"]:,}', inline=True)
        embed.add_field(name='Tử vong', value=data['deceased'], inline=True)
        embed.add_field(name='Phục hồi', value=f'{data["recovered"]:,}', inline=True)

        dt = datetime.strptime(data['lastUpdatedAtSource'], '%Y-%m-%dT%H:%M:%S.%fZ')
        last_updated = dt.timestamp()
        now = datetime.now().timestamp()
        offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)
        diff = now - last_updated - offset.total_seconds()

        vl = ''
        
        if diff >= 3600:
            vl = f'{int(diff//3600)} giờ trước'
        elif diff >= 60:
            vl = f'{int(diff//60)} phút trước'
        else:
            vl = 'vài giây trước'

        embed.add_field(name='Cập nhật gần nhất', value=vl)
        await message.channel.send(embed=embed)

        # Create charts
        # check if image exist first
        filename = f'{dt.strftime("%Y-%m-%dT%H:%M")}.png'
        path = f'covid_charts/{filename}'
        if os.path.exists(path):
            await message.channel.send(file=discord.File(path))
        else:
            with open('provinces_code.json') as f:
                json_data = json.load(f)

            provinces, infecteds, deaths, recovereds = [], [], [], []

            for province in data['detail'][:5]:
                death, recovered, code, infected = province.values()
                provinces.append(json_data.get(code, '?'))
                infecteds.append(infected)
                # recovereds.append(recovered)
                # deaths.append(death)

            plt.bar(provinces, infecteds, color=(1, .5, .5, 0.9))
            plt.title('Top 5 tỉnh/thành phố có nhiều ca mắc nhất')
            plt.xlabel('Tỉnh/Thành phố')
            plt.ylabel('Số ca mắc')
            plt.savefig(path)
            plt.close()

            await message.channel.send(file=discord.File(path))


    if message_content == 'bot ngu' or message_content.startswith('bot ngu'):
        messages = ['ngu cc. vào mà làm bot', 'vâng. bạn thông minh nhất', 'bạn là nhất rồi', 'sủa']
        await message.channel.send(random.choice(messages))
    

    if message_content == 'dlpl':
        await message.channel.send("!play https://www.youtube.com/playlist?list=PL8ZD0D4lXAriRazkWrqUo_3m0XiyqavuA")

    if message_content == 'meme':
        await message.channel.send('Không lưu meme nữa. Nặng quá!')
    
    if message_content == "game":
        if random.randint(1, 10) % 2 == 0 or id_dict.get(author, '') == 'me':
            await message.channel.send("game nào")
        else:
            await message.channel.send("nghiện")

    if 'lô' in words or "alo" in words or 'alô' in words:
        messages = [['@everyone alô alô. chơi game nào'],\
                    ['lô cc'], ['lại tính rủ chơi gêm chứ gì. t hiểu tụi mày quá', 'để t rủ cho', '@everyone gem nào các giáo sư'], \
                        ['lô cc gì mà lô'], ['?']]
        l = random.choice(messages)
        for m in l:
            await message.channel.send(m)
            
    if message_content == '(:':
            await message.channel.send('Bớt thả icon đê!!!!')
            
    if message_content == ':))':
            await message.channel.send('Quân ngu')
            
    if message_content == 'quân':
        await message.channel.send('đầu bùi')
        
    if message_content == 'chửi':
        if random.randint(1, 10) % 2 == 0 
            await message.channel.send('Ai chửi lộn vậy cho tui tham gia với cho vui đê!!!')
        else:
            await message.channel.send("thích thì chửi k thích thì chửi")
            
     if message_content == 'bot chửi':
        if random.randint(1, 10) % 2 == 0 
            await message.channel.send("Tao đã biết chửi ai đâu")
             else:
            await message.channel.send("thích thì chửi k thích thì chửi")
            
              if message_content == 'xạo':
            await message.channel.send('Xạo l k có gì zui chúng ta k nên xạo l')
            
             if message_content == 'bot':
        await message.channel.send('Đứa nào kêu tên bố mày')
        return

    # Bad word
    if message_content in bad_word:
        temp = random.choice(bad_word_response)
        if temp[0] == '|':
            await message.channel.send(file=discord.File(temp[1:]))
        else:
            await message.channel.send(temp)

    if author in id_dict:
        if id_dict[author] != 'me':
            if random.randint(1, 5) == 1:
                await message.channel.send(random.choice(id_dict[author]))
                return

    if random.randint(1, 100) == 10:
        await message.channel.send('😏')
        


load_dotenv()
client.run(os.getenv("TOKEN"))
