import discord, requests, subprocess, json

from src.items import *
from src.utils import *

class Config:
    admins = ['1099019888145727488', '1100211506576097360', '908558131414597634', '364049733058297866', '1085795101730689046', '264271565087178753', '931025746682601483', '1090225338182815744']
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

        if msg == f"{Config.prefix}start":
            """ The Start Of Bot """
            await message.channel.send("YoMarket v2.0 Under Development")

        if msg == f"{Config.prefix}help":
            """ Help Command """
            await self.client.send_embed_w_fields("Help", "List Of Commands!", Config.help_list, "")

        # if f"{Config.prefix}kick": 
        #     # user = discord.utils.get(message.guild.members, id=f"{msg_args[1]}")
        #     # await message.guild.kick(user, reason='Kicked By YoMarket')
        #     # await message.channel.send("User Kicked")

        #     guild = await client.fetch_guild('1088677293997690961')
        #     member = await guild.fetch_member('908558131414597634')
        #     await member.kick(reason='Fuck right off')

        # if f"{Config.prefix}selfrole":
        #     # member = message.author
        #     # role = get(message.guild.roles, name = "CEO")
        #     # await member.add_roles(role, atomic=True)
        #     guild = ctx.guild # You can remove this if you don't need it for something other
        #     role = ctx.guild.get_role(1088694804097028147)
        #     await message.author.add_roles(role)


        if f"{Config.prefix}change" in msg:
            """ Change Item Price Command """
            # if not f"{message.author.id}" in Config.admins: 
            #     await self.client.send_embed_w_fields("Price Change | Error", f"You do not have access to this command....! Contact the owner for access", {}, "");
            #     return;

            if len(msg_args) != 3:
                await self.client.send_embed_w_fields("Price Change | Error", f"Invalid arguments provided....!\nExample Usage: {Config.prefix}change 26295 300m", {}, "");
                return
            item_id = msg_args[1];
            new_price = msg_args[2];
            eng = YoworldItems();
            check_change = eng.change_price(item_id, new_price);
            if check_change == False:
                await self.client.send_embed_w_fields("Price Change | Error", f"[x] Something went wrong changing item price....!\nContact owner for more details.....", {}, "");
                return;
            await self.client.send_embed_w_fields("Price Change", "Item has been successfully updated.....!", {}, "");

        elif f"{Config.prefix}search" in msg:
            if f"{message.guild.id}" != "908592606634729533":
                await message.channel.send("This bot can only be used in 'YoPriceGuide | PNKM's server!\n\ndiscord.gg/bvg")
                print(f"Someone In > {message.guild.name}' is trying to use this bot.....!")
                return
            
            """ Search Command """
            name = msg.replace(f"{msg_args[0]} ", "")
            if len(msg_args) < 2:
                await self.client.send_embed_w_fields("Search Error", f"Invalid item name or ID provided....!\n__Usage:__ ``{Config.prefix}search <item_name/id>", {}, "")

            found = YoworldItems.searchItems(name)
            await self.client.send_embed_w_fields("Search", "Searching, please wait.....!", {}, "")

            if len(found) == 1 and found[0].name == "":
                return (await self.client.send_embed_w_fields("Search", "No items were found....!", {}, ""))
            
            if len(found) == 1:
                info = {"Item Name": found[0].name, "Item ID": str(found[0].iid), "Item Price": found[0].price, "Last Updated On": found[0].last_update, "Yoworld.Info Price": found[0].yoworld_price, "Yoword.Info Last Update": found[0].yoworld_update}
                await self.client.send_item_embed("Search", f"Item Found!", info, found[0].url.strip());
                if name.isdigit(): 
                    ywdb = YoworldItems.advanceInfo(name);
                    await self.client.send_embed_w_fields("Search", "Extra Item Information", ywdb, "");
                return;
        
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
client.run('MTEwNDI1MDAxMzgzNzcwOTQyMg.Gp52Ne.rL0CxxChAqEFkwwv1ykdMNvtjyEJARl7pmKOQ8')

