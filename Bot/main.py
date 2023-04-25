import discord, requests, subprocess, json

from src.items import *
from src.utils import *

class Config:
    prefix = "."
    help_list = {"List of help commands ( This Message )": [f"{prefix}help", False],
                 "Item Search": [f"{prefix}item <item_name/id>", False],
                 "Advance Item Search": [f"{prefix}ai <item_id>", False],
                 "YC Converter": [f"{prefix}yc2c <yc>", False],
                 "WTB Post": [f"{prefix}wtb <item_id> <offer_price>", False],
                 "FS Post": [f"{prefix}fs <item_id> <selling_for_price>", False],
                 "PC Post": [f"{prefix}pc <item_id>", False]}

def _getItemInfo(item_id: str) -> str:
    try:
        item_data = requests.get(f"https://api.yoworld.info/api/items/{item_id}").text
        json_data = json.loads(item_data)['data']['item']['price_proposals']
        return f"{json_data[0]}".replace("{", "").replace("}", "").replace("\':\'", ": ").replace("'", "").replace(", ", "\n").split("\n")[6].replace("price: ", "").strip()
    except:
        return "n/a"

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"[ + ] {self.user} successfully loaded up.....")
        
    async def on_message(self, message):
        msg = message.content
        msg_args = (message.content).split(" ")
        self.client = MessageUtils(message)

        if message.author == self.user: return
        if msg.startswith(Config.prefix) == False: return

        if msg == f"{Config.prefix}start":
            """ The Start Of Bot """
            await message.channel.send("YoMarket v2.0 Under Development")

        if msg == f"{Config.prefix}help":
            """ Help Command """
            await self.client.send_embed_w_fields("Help", "List Of Commands!", Config.help_list, "")

        elif f"{Config.prefix}search" in msg:
            """ Search Command """
            name = msg.replace(f"{msg_args[0]} ", "")
            if len(msg_args) < 2:
                await self.client.send_embed_w_fields("Search Error", f"Invalid item name or ID provided....!\n__Usage:__ ``{Config.prefix}search <item_name/id>", {}, "")

            """ ITEM SEARCH BY NAME """
            found = YoworldItems.searchItems(name)
            if len(found) == 0: 
                return (await self.client.send_embed_w_fields("Search", "No items were found....!", {}, ""))

            if len(found) > 0:
                info = {"Item Name": found[0].name, "Item ID": str(found[0].iid), "Item Price": found[0].price, "Last Updated On": found[0].last_update, "Yoworld.Info Price": found[0].yoworld_price, "Yoword.Info Last Update": found[0].yoworld_update}
                await self.client.send_item_embed("Search", f"Item Found!", info, found[0].url)
            
            if len(found) > 1:
                """ Add results to a dict for embed fields """
                list_of_items = {}
                c = 0
                for item in found:
                    if c == 10: break
                    list_of_items[item.name] = [f"ID: {item.iid} | Price: {item.price} | Updated: {item.last_update}", False]
                    c += 1

                await self.client.send_embed_w_fields("Search", f"A List Of  The {len(found)} items that we found....!", list_of_items, "")
            
            
        print(f"\x1b[31m{message.author}: \x1b[33m{msg}\x1b[0m")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTA5OTk3ODcwNzc0NzIyMTU3Ng.G5pEie.SRkHl1QHuWwrPt5f1gHQlGHyTX44Uy67GBaYeM')
