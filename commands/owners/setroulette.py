# SETROULETTE COMMAND
# envois les parametres de la roulette (les gains et categories)
#setroulette <category/items> : afficher les categories/items de la roulette
#setroulette category <add/remove> : ajouter ou supprimer une categorie
#setroulette items <add/remove> : ajouter ou supprimer un item
# Permission requise : owner

import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class Roulette(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def setroulette(self, ctx,sub: str=None,subsub:str=None):
        if ctx.author.id in self.bot.config["owners"]:
            if sub == None:
                await ctx.send("Veuillez choisir une sous commande : `category` ou `items`")
                return
            if sub == "category":
                if subsub == None:  
                    categories = self.bot.bdd.get_roulette_category()
                    msg = "**Categories de la roulette** \n"
                    for cat in categories:
                        msg += f"__**{cat['id']}**__ : {cat['name']} \n"
                    await ctx.send(embed=interactions.Embed(description=msg))
                    return
                elif subsub == "add":
                    await ctx.send("Veuillez entrer le nom de la categorie a ajouter")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                        msg=await self.bot.wait_for("message_create",timeout=100,checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        return
                    name = msg.message.content
                    self.bot.bdd.add_roulette_category(name)
                    await ctx.send(f"Categorie {name} ajoutée !")
                elif subsub == "remove":
                    await ctx.send("Veuillez entrer l'id de la categorie a supprimer")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                         msg=await self.bot.wait_for("message_create",timeout=100,checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        return
                    try:
                        id = int(msg.message.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre !")
                        return
                    categories = self.bot.bdd.get_roulette_category()
                    if id not in [cat["id"] for cat in categories]:
                        await ctx.send("Cette catégorie n'existe pas !")
                        return
                    self.bot.bdd.remove_roulette_category(id)
                    totalrarity=0
                    for item in self.bot.bdd.get_roulette_items():
                        if item["id"] == 1:
                            continue
                        totalrarity+=item["rarity"]
                    try:
                        self.bot.bdd.remove_roulette_item(1)
                    except:
                        pass
                    categories = self.bot.bdd.get_roulette_category()
                    self.bot.bdd.add_roulette_nothing(1,categories[-1]["id"],100-totalrarity)
                    await ctx.send(f"Categorie {id} supprimée !")


            elif sub=="items":
                if subsub == None:
                    items = self.bot.bdd.get_roulette_items()
                    msg = "**Items de la roulette** \n"
                    for item in items:
                        msg += f"__**{item['id']}**__ : {item['name']} - {item['rarity']}% \n"
                    await ctx.send(embed=interactions.Embed(description=msg))
                    return
                elif subsub == "add":
                    await ctx.send("Veuillez entrer le nom de l'item a ajouter")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                        msg=await self.bot.wait_for("message_create",timeout=100,checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        return
                    name = msg.message.content
                    await ctx.send("Veuillez entrer l'id de la categorie de l'item")
                    try:
                        msg=await self.bot.wait_for("message_create",timeout=100,checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        return
                    try:
                        category = int(msg.message.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre !")
                        return
                    categories = self.bot.bdd.get_roulette_category()
                    if category not in [cat["id"] for cat in categories]:
                        await ctx.send("Cette catégorie n'existe pas !")
                        return
                    await ctx.send("Veuillez entrer le type de l'item (role,badge,coins,jetons)")
                    try:
                        msg=await self.bot.wait_for("message_create",timeout=100,checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        return
                    type = msg.message.content
                    if type not in ["role","badge","coins","jetons"]:
                        await ctx.send("Veuillez entrer un type valide !")
                        return
                    if type == "role" or type == "badge":
                        await ctx.send("Veuillez entrer l'id du role qui serras donné")
                    if type == "coins" or type == "jetons":
                        await ctx.send("Veuillez entrer le nombre de coins/jetons qui serront ajoutés")
                    try:
                        msg=await self.bot.wait_for("message_create",timeout=100,checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        return
                    data = msg.message.content
                    if type == "role" or type == "badge":
                        try:
                            data = int(data)
                            r=ctx.guild.get_role(data)
                            if r is None:
                                await ctx.send("Ce role n'existe pas !")
                                return
                        except:
                            try:
                                data = data.split("<@&")[1].split(">")[0]
                            except:
                                await ctx.send("Veuillez entrer un role valide !")
                                return
                            r=ctx.guild.get_role(int(data))
                            if r is None:
                                await ctx.send("Ce role n'existe pas !")
                                return
                    if type == "coins" or type == "jetons":
                        try:
                            data = int(data)
                        except:
                            await ctx.send("Veuillez entrer un nombre !")
                            return
                        
                    await ctx.send("Veuillez entrer la rareté de l'item (pourcentage)")
                    try:
                        msg=await self.bot.wait_for("message_create",timeout=100,checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        return
                    if "%" in msg.message.content:
                        msg.message.content = msg.message.content.replace("%","")
                    try:
                        rarity = float(msg.message.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre !")
                        return
                    totalrarity=0
                    for item in self.bot.bdd.get_roulette_items():
                        if item["id"] == 1:
                            continue
                        totalrarity+=item["rarity"]
                    if totalrarity+rarity>100:
                        await ctx.send("La somme totale des raretés des items ne peut pas dépasser 100% !")
                        return
                    else:
                        try:
                            self.bot.bdd.remove_roulette_item(1)
                        except:
                            pass
                        categories = self.bot.bdd.get_roulette_category()
                        print(categories[-1]["id"])
                        self.bot.bdd.add_roulette_nothing(1,categories[-1]["id"],100-totalrarity-rarity)
                    self.bot.bdd.add_roulette_item(category,name,type,data,rarity)
                    await ctx.send(f"Item {name} ajouté !")



                elif subsub == "remove":
                    await ctx.send("Veuillez entrer l'id de l'item a supprimer")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                        msg=await self.bot.wait_for("message_create",timeout=100,checks=check)
                    except:
                        await ctx.send("Temps écoulé !")
                        return
                    try:
                        id = int(msg.message.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre !")
                        return
                    if id == 1:
                        await ctx.send("Vous ne pouvez pas supprimer cet item qui est géré automatiquement !")
                        return
                    items = self.bot.bdd.get_roulette_items()
                    if id not in [item["id"] for item in items]:
                        await ctx.send("Cet item n'existe pas !")
                        return
                    self.bot.bdd.remove_roulette_item(id)
                    totalrarity=0
                    for item in self.bot.bdd.get_roulette_items():
                        if item["id"] == 1:
                            continue
                        elif item["id"] == id:
                            itemm = item
                        totalrarity+=item["rarity"]
                    try:
                        self.bot.bdd.remove_roulette_item(1)
                    except:
                        pass
                    categories = self.bot.bdd.get_roulette_category()

                    self.bot.bdd.add_roulette_nothing(1,categories[-1]["id"],100-totalrarity)
                    await ctx.send(f"Item {id} supprimé ! \n :warning: Attention ! Si l'ityem etait un badge, les utilisateurs qui l'avaient obtenu l'ont toujours !")
        else:
            await ctx.send("Veuillez choisir une sous commande : `category` ou `items`")