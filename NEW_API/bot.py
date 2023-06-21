import discord, requests, subprocess, json

from src.discord_embed          import *
from src.yoguide.yoguide        import *
from src.yoguide.item_searches  import *

class Config:
    prefix = "!"
    help_list = {"List of help commands ( This Message )": [f"{prefix}help", False],
                 "Item Search": [f"{prefix}item <item_name/id>", False],
                 "Advance Item Search": [f"{prefix}ai <item_id>", False],
                 "YC Converter": [f"{prefix}yc2c <yc>", False],
                 "WTB Post": [f"{prefix}wtb <item_id> <offer_price>", False],
                 "FS Post": [f"{prefix}fs <item_id> <selling_for_price>", False],
                 "PC Post": [f"{prefix}pc <item_id>", False]}

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"[ + ] {self.user} successfully loaded up.....")

    async def on_message(self, message):
        msg = message.content
        msg_args = (message.content).split(" ")
        self.client = MessageUtils(message)

        if message.author == self.user: return
        if msg.startswith(Config.prefix) == False: return

        """
            Command Handler
        """
        if msg == f"{Config.prefix}start":
            """ The Start Of Bot """
            await message.channel.send("YoGuide v3.0 Under Development")

        if msg == f"{Config.prefix}help":
            """ Help Command """
            await self.client.embed_w_fields("Help", "List Of Commands!", Config.help_list, "")

        if f"{Config.prefix}change" in msg:
            """ 
                Command: change
                Usage: change <item_id> <new_price>
            """

        elif f"{Config.prefix}search" in msg:
            """ 
                Command: search
                Usage: search <query>
            """
            query = msg.replace(f"{msg_args[0]} ", "")
            eng = YoGuide();
            check = eng.Search(query);
            results = eng.getResults(check);

            if check == Response.NONE:
                await message.channel.send(embed=discord.Embed(title="YoGuide | Item Search", description="No items found....!", color=discord.Colour.red()));

            if check == Response.EXACT:

                ItemSearch.ywdbSearch(results);
                gg = YoGuide.addInfo(results, YoGuide.item2dict(results));
                await self.client.displayItem("YoGuide | Item Search", "Item found!", gg, results.url);

            elif check == Response.EXTRA:

                item_list = {};
                c = 0;
                for itm in results:
                    item_list[itm.name] = [f"ID: {itm.id} | Price: {itm.price} | Update: {itm.update}", False];
                    c += 1;

                await self.client.embed_w_fields("YoGuide | Item Search", f"{len(results)} Items found....!\n\nPlease note, If you need to view the image... just search the item by its ID listed under the name!", item_list, "https://images-ext-2.discordapp.net/external/-Vpwem0mrDhbSXF7d6otskf8aZRH97gKOT1T549B3xc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1110583722190831688/a77bb0aa24120f8733229797c4564402.png");

            
        print(f"\x1b[31m{message.author}: \x1b[33m{msg}\x1b[0m")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTEyMTA0NDgxNDA3MTM0NTIyMw.GMNQPo.uWOZ3CnLAPOz_xkOMrPWYGbTQRAntq_gDKwlng')

