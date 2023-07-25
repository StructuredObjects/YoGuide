import discord, requests, subprocess, json

from src.logger                 import *
from src.discord_embed          import *
from src.yoguide.yoguide        import *

class Config:
    prefix = "!"
    yc_rate = 60000
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
            
        if f"{Config.prefix}rate" in msg:
            if len(msg_args) != 2:
                await self.client.embed_w_fields("YC Rate Change | Error", f"Invalid arguments provided\nUsage {Config.prefix}rate <yc_rate>", {}, "");
                return;
            
            Config.yc_rate = int(msg_args[1]);
            await self.client.embed_w_fields("YC Rate Change", f"YC Rate successfull5y changed to {msg_args[1]}", {}, "");

        if f"{Config.prefix}yc2c" in msg:
            yc = msg_args[1];
            converted = int(yc)*Config.yc_rate;
            await self.client.embed_w_fields("YC 2 Coins", f"{yc}yc x {Config.yc_rate} = {converted}", {}, "");

        if f"{Config.prefix}fs" in msg:
            """ 
                Command: fs
                Usage: fs <item_id> <fs_price> 
            """
            if len(msg_args) < 2:
                await self.client.embed_w_fields("fs | Error", "Ivalid arguments provided\nUsage: 26295 290m");
                return;

            iid = msg_args[1];
            price = "n/a";
            if len(msg_args) == 3: price = msg_args[2];

            eng = YoGuide();
            resp = eng.Search(iid);

            if resp == Response.EXACT:
                result = eng.getResults(resp);
                chan = client.get_channel('1083572855830237185');
                gg = MessageUtils(message).createEmbed("WTB", f"User: <@{message.author.id}> is selling > '{result.name}'", YoGuide.item2dict(result), result.url)
                await chan.send(embed=gg);
                # await self.client.displayItem("WTB", f"User: <@{message.author.id}> want's to buy '{result.name}'", YoGuide.item2dict(result), "", channel);
                

        # if msg == f"{Config.prefix}wtb"

        if f"{Config.prefix}change" in msg:
            """ 
                Command: change
                Usage: change <item_id> <new_price>
            """

            if f"{message.guild.id}" != "908592606634729533" and f"{message.guild.id}" != "1110583722190831688":
                await message.channel.send(embed=discord.Embed(title="YoGuide | Price Change", description="Error, You can only change prices using this command in 'YoPriceGuide | PNKM' discord server!", color=discord.Colour.red()));
                await message.channe.send("https://discord.gg/pnkm");
                return

            if len(msg_args) != 3:
                await message.channel.send(embed=discord.Embed(title="YoGuide | Price Change", description="Error, You must provide an item ID and new price...!\nUsage: !change <item_id> <new_price>\nExample #1: !change 26295 290m", color=discord.Colour.red()));
                return

            item_id = msg_args[1];
            new_price = msg_args[2];

            if not YoGuide.isID(item_id):
                await self.client.embed_w_fields("YoGuide | Change", "Invalid item ID provided....\nUsage: !change <item_id> <new_price>\nExample: !change 26295 290m", {}, "");
                return;

            eng = YoGuide();
            check = eng.Search(item_id);
            
            if check != Response.EXACT:
                await self.client.embed_w_fields("YoGuide | Change", "Item was not found... Must be an invalid item ID!", {}, "");
                return;

            r = eng.getResults(check);

            if not YoGuide.changePrice(r, new_price):
                await self.client.embed_w_fields("YoGuide | Change", "Item could not be updated....! Contact owner for more info.", {}, "");
                return;
        
            Logger.newLog(AppType.BOT, LogTypes.CHANGE, item_id, f"{message.author.id}");

            await self.client.embed_w_fields("YoGuide | Change", f"Item: {r.name} sucessfully updated!", {}, "");

        elif f"{Config.prefix}update" in msg:
            lst = msg.replace(f"{msg_args[0]} ", "").replace("```", "");
        
            chk, failed, changed = YoGuide.bulk_update(lst);
            await self.client.embed_w_fields("YoGuide | Bulk Update", f"Results for the following list of items to update:\n\n```{lst}```", {"Update Status": [chk, False], "Items Failed To Update": [failed, False], "Successfully Updated Items": [changed, False]}, "https://images-ext-2.discordapp.net/external/-Vpwem0mrDhbSXF7d6otskf8aZRH97gKOT1T549B3xc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1110583722190831688/a77bb0aa24120f8733229797c4564402.png");
        

        elif msg == f"{Config.prefix}search" or msg == f"{Config.prefix}search ": await message.channel.send(embed=discord.Embed(title="YoGuide | Item Search", description="Error, You must provide a item name or item ID...!\nUsage: !search <item_name_or_id>\nExample #1: !search cupids wing\nExample #2: !search 26295", color=discord.Colour.red()));
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

                try: ItemSearch.ywdbSearch(results);
                except: print("[ X ] Error, Unable to fetch extra info....!");
                
                gg = YoGuide.addInfo(results, YoGuide.item2dict(results));
                await self.client.displayItem("YoGuide | Item Search", "Item found!", gg, results.url);

            elif check == Response.EXTRA:

                item_list = {};
                c = 0;
                for itm in results:
                    item_list[itm.name] = [f"ID: {itm.id} | Price: {itm.price} | Update: {itm.update}", False];
                    c += 1;

                await self.client.embed_w_fields("YoGuide | Item Search", f"{len(results)} Items found....!\n\nPlease note, If you need to view the image... just search the item by its ID listed under the name!", item_list, "https://images-ext-2.discordapp.net/external/-Vpwem0mrDhbSXF7d6otskf8aZRH97gKOT1T549B3xc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1110583722190831688/a77bb0aa24120f8733229797c4564402.png");
        
            
            Logger.newLog(AppType.BOT, LogTypes.SEARCH, query, "NONE");

            
        print(f"\x1b[31m{message.author}: \x1b[33m{msg}\x1b[0m")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTEyMTA0NDgxNDA3MTM0NTIyMw.GwiNKV.K4C-IdE3VbLXraHj8IvQb8Au52N0-E6e0X3GFI')

