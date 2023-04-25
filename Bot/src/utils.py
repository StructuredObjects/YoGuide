import discord

class MessageUtils():
    def __init__(self, c):
        self.client = c

    async def send_embed_w_fields(self, title: str, description: str, fields: dict, image_url: str) -> bool:
        if title == "": return False; 
        if description == "": return False;
        embed = discord.Embed(title=f"{title}", description=f"{description}", color=discord.Colour.red());

        for key in fields:
            embed.add_field(name=f"{key}", value=f"{fields[key][0]}", inline=fields[key][1]);
            
        if image_url: embed.set_image(url=f"{image_url}");
        await self.client.channel.send(embed=embed);
        return True

    async def send_item_embed(self, t: str, desc: str, fields: dict, iurl: str) -> None:
        embed = discord.Embed(title=f"{t}", description=f"{desc}", color=discord.Colour.red())

        for key in fields:
            embed.add_field(name=f"{key}", value=f"{fields[key]}", inline=True)

        if iurl: embed.set_image(url=f"{iurl}")
        await self.client.channel.send(embed=embed)
