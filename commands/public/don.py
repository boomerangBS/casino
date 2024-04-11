# DON COMMAND
#don <user> <montant>
# donne <montant> - taxe de 10% coins à l'utilisateur ciblé
# minimum 10 coins

import interactions,random
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime,timedelta

class Don(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def don(self, ctx, user=None, montant=None):
        bdd=self.bot.bdd
        if user == None or montant == None:
            await ctx.send("Vous devez mentionner un utilisateur et un montant !")
            return
        try:
            user = int(user)
        except:
            try:
                user = int(user.split("<@")[1].split(">")[0])
            except:
                await ctx.send("Utilisateur invalide !")
                return
        try:
            montant = int(montant)
        except:
            await ctx.send("Montant invalide !")
            return
        if montant < 10:
            await ctx.send("Le montant minimum est de 10 coins !")
            return
        if user == ctx.author.id:
            await ctx.send("Vous ne pouvez pas vous donner des coins à vous même !")
            return
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            if u["coins"] < montant:
                await ctx.send("Vous n'avez pas assez de coins !")
                return
            console.log(f"don | {ctx.author} ({ctx.author.id})")
            u2 = bdd.check_user(user)
            if u2 != []:
                u2 = u2[0]
                bdd.set_coins(u["coins"]-montant,ctx.author.id)
                bdd.set_coins(u2["coins"]+montant-montant/10,user)
                await ctx.send(f"<@{ctx.author.id}> a donné {montant-montant/10} coins à <@{user}> !")
            else:
                await ctx.send("Cet utilisateur n'est pas inscrit sur le bot !")
        else:
            await ctx.send("Utilisateur invalide !")