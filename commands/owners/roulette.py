# ROULETTE COMMAND

#categories (category) : affiche les catégories de la roulette
#items (item): affiche les items de la roulette

# Permission requise : owner

import interactions, asyncio
from interactions import Extension, Button, ButtonStyle,component_callback
from interactions.ext.prefixed_commands import prefixed_command
from utils import console


class Roulette(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command(aliases=["category"])
    async def categories(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            console.log(f"categories | {ctx.author} ({ctx.author.id})")
            while True:
                categories = self.bot.bdd.get_roulette_category()
                msg = "**Catégories de la roulette** \n"
                for cat in categories:
                    msg += f"__**{cat['id']}**__ : {cat['name']} \n"
                embed = interactions.Embed(description=msg)
                butttons = [Button(style=ButtonStyle.PRIMARY, label="Ajouter une catégorie", custom_id="addcategory"), Button(style=ButtonStyle.DANGER, label="Supprimer une catégorie", custom_id="delcategory")]
                if "m" in locals():
                    await m.edit(embed=embed,components=[butttons])
                else:
                    m=await ctx.send(embed=embed,components=[butttons])
                try:
                    interaction = await self.bot.wait_for_component(components=butttons, timeout=100, check=lambda i: i.ctx.author == ctx.author and i.ctx.message == m)
                except asyncio.TimeoutError:
                    await ctx.send("Temps écoulé !")
                    await m.edit(components=[])
                    return
                except Exception as e:
                    console.error(e)
                    await ctx.send("Une erreur est survenue !")
                    await m.edit(components=[])
                    return
                interaction=interaction.ctx

                if interaction.custom_id == "addcategory":
                    console.log(f"addcategory | {ctx.author} ({ctx.author.id})")
                    first=await interaction.send(":hourglass: Veuillez maintenant envoyer le nom de la catégorie à ajouter")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for("message_create", timeout=100, checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        continue
                    name = msg.message.content
                    await first.delete()
                    await msg.message.delete()
                    self.bot.bdd.add_roulette_category(name)
                    await ctx.send(f"Catégorie {name} ajoutée !")


                if interaction.custom_id == "delcategory":
                    console.log(f"delcategory | {ctx.author} ({ctx.author.id})")
                    first=await interaction.send(":hourglass: Veuillez maintenant envoyer l'id de la catégorie à supprimer")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for("message_create", timeout=100, checks=check)
                        id = int(msg.message.content)
                    except:
                        await ctx.send("Temps écoulé !")
                        continue
                    if id not in [cat["id"] for cat in categories]:
                        await ctx.send("Cette catégorie n'existe pas !")
                        continue
                    self.bot.bdd.remove_roulette_category(id)
                    totalrarity = 0
                    for item in self.bot.bdd.get_roulette_items():
                        if item["id"] == 1:
                            continue
                        totalrarity += item["rarity"]
                    try:
                        self.bot.bdd.remove_roulette_item(1)
                    except:
                        pass
                    categories = self.bot.bdd.get_roulette_category()
                    self.bot.bdd.add_roulette_nothing(1, categories[-1]["id"], 100 - totalrarity)
                    await first.delete()
                    await msg.message.delete()
                    await ctx.send(f"Catégorie {id} supprimée !")
        


    @prefixed_command(aliases=["items"])
    async def item(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            console.log(f"items | {ctx.author} ({ctx.author.id})")
            while True:
                items = self.bot.bdd.get_roulette_items()
                msg = "**Items de la roulette** \n"
                for item in items:
                    msg += f"__**{item['id']}**__ : {item['name']} - {item['rarity']}% \n"
                embed = interactions.Embed(description=msg)
                buttons = [Button(style=ButtonStyle.PRIMARY, label="Ajouter un item", custom_id="additem"), Button(style=ButtonStyle.DANGER, label="Supprimer un item", custom_id="delitem")]
                if "m" in locals():
                    await m.edit(embed=embed,components=[buttons])
                else:
                    m=await ctx.send(embed=embed,components=[buttons])
                try:
                    interaction = await self.bot.wait_for_component(components=buttons, timeout=100, check=lambda i: i.ctx.author == ctx.author and i.ctx.message == m)
                except asyncio.TimeoutError:
                    await ctx.send("Temps écoulé !")
                    await m.edit(components=[])
                    return
                except Exception as e:
                    console.error(e)
                    await ctx.send("Une erreur est survenue !")
                    await m.edit(components=[])
                    return
                interaction=interaction.ctx
                if interaction.custom_id == "additem":
                    console.log(f"additem | {ctx.author} ({ctx.author.id})")
                    first=await interaction.send("Veuillez entrer le nom de l'item à ajouter")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for("message_create", timeout=100, checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        continue
                    await first.delete()
                    await msg.message.delete()
                    name = msg.message.content
                    mm=await ctx.send("Veuillez entrer l'id de la catégorie de l'item")
                    try:
                        msg = await self.bot.wait_for("message_create", timeout=100, checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        continue
                    try:
                        category = int(msg.message.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre !")
                        continue
                    await mm.delete()
                    await msg.message.delete()
                    categories = self.bot.bdd.get_roulette_category()
                    if category not in [cat["id"] for cat in categories]:
                        await ctx.send("Cette catégorie n'existe pas !")
                        continue
                    mm=await ctx.send("Veuillez entrer le type de l'item (role, badge, coins, jetons)")
                    try:
                        msg = await self.bot.wait_for("message_create", timeout=100, checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        continue
                    await mm.delete()
                    await msg.message.delete()
                    type = msg.message.content
                    if type not in ["role", "badge", "coins", "jetons"]:
                        await ctx.send("Veuillez entrer un type valide !")
                        continue
                    if type == "role" or type == "badge":
                        mm=await ctx.send("Veuillez entrer l'id du rôle qui sera donné")
                    if type == "coins" or type == "jetons":
                        mm=await ctx.send("Veuillez entrer le nombre de coins/jetons qui seront ajoutés")
                    try:
                        msg = await self.bot.wait_for("message_create", timeout=100, checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        continue
                    await mm.delete()
                    await msg.message.delete()
                    data = msg.message.content
                    if type == "role" or type == "badge":
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
                    if type == "coins" or type == "jetons":
                        try:
                            data = int(data)
                        except:
                            await ctx.send("Veuillez entrer un nombre !")
                            continue
                    mm=await ctx.send("Veuillez entrer la rareté de l'item (pourcentage)")
                    try:
                        msg = await self.bot.wait_for("message_create", timeout=100, checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        continue
                    await mm.delete()
                    await msg.message.delete()
                    if "%" in msg.message.content:
                        msg.message.content = msg.message.content.replace("%", "")
                    try:
                        rarity = float(msg.message.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre !")
                        continue
                    totalrarity = 0
                    for item in self.bot.bdd.get_roulette_items():
                        if item["id"] == 1:
                            continue
                        totalrarity += item["rarity"]
                    if totalrarity + rarity > 100:
                        await ctx.send("La somme totale des raretés des items ne peut pas dépasser 100% !")
                        continue
                    else:
                        try:
                            self.bot.bdd.remove_roulette_item(1)
                        except:
                            pass
                        categories = self.bot.bdd.get_roulette_category()
                        self.bot.bdd.add_roulette_nothing(1, categories[-1]["id"], 100 - totalrarity - rarity)
                    self.bot.bdd.add_roulette_item(category, name, type, data, rarity)
                    await ctx.send(f"Item {name} ajouté !")


                if interaction.custom_id == "delitem":
                    console.log(f"delitem | {ctx.author} ({ctx.author.id})")
                    first=await interaction.send("Veuillez entrer l'id de l'item à supprimer")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for("message_create", timeout=100, checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        continue
                    try:
                        id = int(msg.message.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre !")
                        await first.delete()
                        continue
                    if id == 1:
                        await ctx.send("Vous ne pouvez pas supprimer cet item qui est géré automatiquement !")
                        await first.delete()
                        continue
                    items = self.bot.bdd.get_roulette_items()
                    if id not in [item["id"] for item in items]:
                        await ctx.send("Cet item n'existe pas !")
                        await first.delete()
                        continue
                    self.bot.bdd.remove_roulette_item(id)
                    totalrarity = 0
                    for item in self.bot.bdd.get_roulette_items():
                        if item["id"] == 1:
                            continue
                        elif item["id"] == id:
                            itemm = item
                        totalrarity += item["rarity"]
                    try:
                        self.bot.bdd.remove_roulette_item(1)
                    except:
                        pass
                    categories = self.bot.bdd.get_roulette_category()

                    self.bot.bdd.add_roulette_nothing(1, categories[-1]["id"], 100 - totalrarity)
                    await first.delete()
                    await msg.message.delete()
                    await ctx.send(f"Item {id} supprimé ! \n :warning: Attention ! Si l'item était un badge, les utilisateurs qui l'avaient obtenu l'ont toujours !")