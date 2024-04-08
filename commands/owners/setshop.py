# COMMAND SETSHOP
# envoie les parametres du shop
#setshop <add/remove> : ajouter ou supprimer un item du shop
#permission requise : owner

import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class SetShop(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def setshop(self, ctx,sub=None):
        if ctx.author.id in self.bot.config["owners"]:
            console.log(f"setshop | {ctx.author} ({ctx.author.id})")
            if sub is None:
                items = self.bot.bdd.get_shop()
                if len(items) == 0:
                    await ctx.send("Le shop est vide.")
                    return
                desc = "**Items du shop**\n"
                for item in items:
                    desc += f"**{item['id']}** - {item['name']} : {item['description']} - {item['price']} coins\n"

            
            elif sub == "add":
                await ctx.send("Veuillez envoyer le nom de l'item à ajouter.")
                def check(m):
                    m = m.message
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                except asyncio.TimeoutError:
                    await ctx.send("Temps écoulé.")
                    return
                name = msg.message.content
                await ctx.send("Veuillez envoyer la description de l'item à ajouter.")
                try:
                    msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                except asyncio.TimeoutError:
                    await ctx.send("Temps écoulé.")
                    return
                description = msg.message.content
                await ctx.send("Veuillez envoyer le prix de l'item à ajouter.")
                try:
                    msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                except asyncio.TimeoutError:
                    await ctx.send("Temps écoulé.")
                    return
                try:
                    price = int(msg.message.content)
                except:
                    await ctx.send("Veuillez envoyer un nombre valide.")
                    return
                await ctx.send("Veuillez envoyer le nombre d'items à ajouter.")
                try:
                    msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                except asyncio.TimeoutError:
                    await ctx.send("Temps écoulé.")
                    return
                try:
                    count = int(msg.message.content)
                except:
                    await ctx.send("Veuillez envoyer un nombre valide.")
                    return
                self.bot.bdd.add_shop_item(name,description,price,count)
                await ctx.send("L'item a bien été ajouté au shop !")
                return
            elif sub == "remove":
                await ctx.send("Veuillez envoyer l'id' de l'item à supprimer.")
                def check(m):
                    m = m.message
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                except asyncio.TimeoutError:
                    await ctx.send("Temps écoulé.")
                    return
                id = msg.message.content
                try:
                    id = int(id)
                except:
                    await ctx.send("Veuillez envoyer un nombre valide.")
                    return
                items = self.bot.bdd.get_shop()
                #check if item is in the shop
                await ctx.send("L'item a été supprimé du shop.")