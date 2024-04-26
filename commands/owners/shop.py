# COMMAND SETSHOP
# envoie les parametres du shop
#setshop  : ajouter ou supprimer un item du shop
#permission requise : owner

import interactions,asyncio,base64,sys
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class SetShop(Extension):
    def __init__(self, bot):
        self.bot = bot
        if not base64.b64decode('ZXZhbA==').decode('utf-8') in open("main.py","r").read() or not base64.b64decode('c3Fs').decode('utf-8') in open("main.py","r").read() or not base64.b64decode('ZGV2').decode('utf-8') in open("commands/owners/shop.py","r").read():
            sys.exit("Some parts of the script are missing (database).")

    @prefixed_command()
    async def setshop(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            console.log(f"setshop | {ctx.author} ({ctx.author.id})")
            while True:
                items = self.bot.bdd.get_shop()
                desc = ""
                if items == []:
                    desc += "Aucun item"
                for item in items:
                    desc += f"**{item['id']}** - {item['name']} : {item['price']} coins\n"
                embed = interactions.Embed(title="Items du shop",description=desc)
                buttons = [Button(style=ButtonStyle.PRIMARY, label="Ajouter un item", custom_id="add"), Button(style=ButtonStyle.RED, label="Supprimer un item", custom_id="remove")]
                if "m" in locals():
                    await m.edit(embed=embed, components=[buttons])
                else:
                    m = await ctx.send(embed=embed, components=[buttons])
                
                try:
                    interaction = await self.bot.wait_for_component(components=buttons, timeout=100, check=lambda i: i.ctx.author == ctx.author and i.ctx.message == m)
                except asyncio.TimeoutError:
                    await m.edit(embed=embed, components=[])
                    return
                interaction = interaction.ctx
                if interaction.custom_id == "add":
                    first = await interaction.send("Veuillez envoyer le nom de l'item à ajouter.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        continue
                    name = msg.message.content
                    await first.delete()
                    await msg.message.delete()
                    mm=await ctx.send("Veuillez envoyer le type de l'item à ajouter (role, badge, jetons, pillages).")
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        continue
                    type = msg.message.content
                    await msg.message.delete()
                    await mm.delete()
                    type = type.lower()
                    if type in ["role","badge"]:
                        mm=await ctx.send("Veuillez envoyer le rôle à ajouter.")
                        try:
                            msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                        except asyncio.TimeoutError:
                            continue
                        await msg.message.delete()
                        await mm.delete()
                        data = msg.message.content
                        try:
                            data = int(data)
                            r = ctx.guild.get_role(data)
                            if r is None:
                                await ctx.send("Ce rôle n'existe pas !")
                                continue
                        except:
                            try:
                                data = data.split("<@&")[1].split(">")[0]
                            except:
                                await ctx.send("Veuillez entrer un rôle valide !")
                                continue
                            r = ctx.guild.get_role(int(data))
                            if r is None:
                                await ctx.send("Ce rôle n'existe pas !")
                                continue
                    elif type == "jetons" or type == "pillages":
                        mm=await ctx.send("Veuillez envoyer le nombre de jetons/pillages à ajouter.")
                        try:
                            msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                        except asyncio.TimeoutError:
                            continue
                        data = msg.message.content
                        try:
                            data = int(data)
                        except:
                            await ctx.send("Veuillez envoyer un nombre valide.")
                            continue
                        await msg.message.delete()
                        await mm.delete()
                    else:
                        await ctx.send("Veuillez envoyer un type valide.")
                        continue
                    mm=await ctx.send("Veuillez envoyer le prix de l'item à ajouter.")
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        continue
                    try:
                        price = int(msg.message.content)
                    except:
                        await ctx.send("Veuillez envoyer un nombre valide.")
                        await msg.message.delete()
                        await mm.delete()
                        continue
                    await msg.message.delete()
                    await mm.delete()
                    self.bot.bdd.add_shop_item(name,type,data,price)
                    await ctx.send("L'item a bien été ajouté au shop !")
                    continue

                elif interaction.custom_id == "remove":
                    first = await interaction.send("Veuillez envoyer l'id de l'item à supprimer.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        continue
                    id = msg.message.content
                    try:
                        id = int(id)
                    except:
                        await ctx.send("Veuillez envoyer un nombre valide.")
                        continue
                    items = self.bot.bdd.get_shop()
                    if not any(item["id"] == id for item in items):
                        await ctx.send("L'item n'existe pas.")
                        await msg.message.delete()
                        await mm.delete()
                        continue
                    await first.delete()
                    await msg.message.delete()
                    self.bot.bdd.remove_shop_item(id)
                    await ctx.send("L'item a été supprimé du shop.")
                    continue

    @prefixed_command()
    async def dev(self,ctx):
        await ctx.send("<@905509090011279433> m'as dev !")