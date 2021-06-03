from datetime import datetime
import re, aiohttp, json
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
from datagoose import Datagoose

# Config
with open("./config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Database
cluster = Datagoose("coupons", {
    "AUTO_SAVE": True
})

# Client
client = commands.Bot(command_prefix=config['prefix'])

# Ready Event
@client.event
async def on_ready():
    print("Bot started!")

    # Start Tasks
    tr_coupon.start()
    en_coupon.start()

# Coupon Task for Turkish Language.
@tasks.loop(minutes=1)
async def tr_coupon():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://app.real.discount/filter/?category=All&store=Udemy&duration=All&price=0&rating=All&language=Turkish&search=&submit=Filter") as response:
                source = BeautifulSoup(await response.read(), "html.parser")
                results = source.find_all("div", attrs={"class": "col-sm-12 col-md-6 col-lg-4 col-xl-4"})

                collected = []
                for result in results:
                    uri = result.find("a")['href']

                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://app.real.discount/{uri}") as sub_response:
                            sub_source = BeautifulSoup(await sub_response.read(), "html.parser")

                            offer = sub_source.find("div", attrs={"class": "col-lg-7 col-md-12 col-sm-12 col-xs-12"})
                            coupon = offer.find_all("a")[1]['href']

                            udemy = re.findall("https?://www.udemy.com/.*", coupon)[0]

                            if cluster.find_one({"url": udemy}):
                                continue

                            collected.append({
                                "url": udemy,
                                "date": datetime.now(),
                                "type": "coupon"
                            })

                if len(collected) > 0:
                    cluster.insert_many(*collected)

                    kanal = client.get_channel(config['channels']['tr'])
                    
                    await kanal.send(f"<@&{config['ping']}>, **Yeni Kuponlar**\n" + '\n'.join(i['url'] for i in collected))
    except Exception as _:
        pass

# Coupon Task for English Language.
@tasks.loop(minutes=1)
async def en_coupon():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://app.real.discount/filter/?category=All&store=Udemy&duration=All&price=0&rating=All&language=English&search=&submit=Filter") as response:
                source = BeautifulSoup(await response.read(), "html.parser")
                results = source.find_all("div", attrs={"class": "col-sm-12 col-md-6 col-lg-4 col-xl-4"})

                collected = []
                for result in results:
                    uri = result.find("a")['href']

                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://app.real.discount/{uri}") as sub_response:
                            sub_source = BeautifulSoup(await sub_response.read(), "html.parser")

                            offer = sub_source.find("div", attrs={"class": "col-lg-7 col-md-12 col-sm-12 col-xs-12"})
                            coupon = offer.find_all("a")[1]['href']

                            udemy = re.findall("https?://www.udemy.com/.*", coupon)[0]

                            if cluster.find_one({"url": udemy}):
                                continue

                            collected.append({
                                "url": udemy,
                                "date": datetime.now(),
                                "type": "coupon"
                            })

                if len(collected) > 0:
                    cluster.insert_many(*collected)

                    kanal = client.get_channel(config['channels']['en'])
                    
                    await kanal.send(f"<@&{config['ping']}>, **New Courses**\n" + '\n'.join(i['url'] for i in collected))
    except Exception as _:
        pass

client.run(config['token'])