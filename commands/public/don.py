# DON COMMAND
#don <user> <montant>
# donne <montant> - taxe de 10% coins à l'utilisateur ciblé
# minimum 10 coins

import interactions,random
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console,generate_log_embed
from datetime import datetime,timedelta

class Don(Extension):
    def __init__(self, bot):
        self.bot = bot
    @prefixed_command()
    async def don(self, ctx, user=None, montant=None):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    await ctx.reply("Cette commande n'est pas autorisée dans ce salon !")
                    return
        bdd=self.bot.bdd
        if user == None or montant == None:
            await ctx.reply("Vous devez mentionner un utilisateur et un montant !")
            return
        try:
            user = int(user)
        except:
            try:
                user = int(user.split("<@")[1].split(">")[0])
            except:
                await ctx.reply("Utilisateur invalide !")
                return
        try:
            montant = int(montant)
        except:
            await ctx.reply("Montant invalide !")
            return
        if montant < 10:
            await ctx.reply("Le montant minimum est de 10 coins !")
            return
        if user == ctx.author.id:
            await ctx.reply("Vous ne pouvez pas vous donner des coins à vous même !")
            return
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            if u["coins"] < montant:
                await ctx.reply("Vous n'avez pas assez de coins !")
                return
            console.log(f"don | {ctx.author} ({ctx.author.id})")
            u2 = bdd.check_user(user)
            if u2 != []:
                u2 = u2[0]
                bdd.set_coins(u["coins"]-montant,ctx.author.id)
                bdd.set_coins(u2["coins"]+int(montant-montant/10),user)
                embed = interactions.Embed(title=":moneybag: Don",description=f"Vous avez donné {"{:,}".format(int(montant-montant/10))} coins à <@{user}> !")
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a donné {"{:,}".format(int(montant))} coins (hors taxes) à <@{user}>")
                await generate_log_embed(self.bot,f"<@{user}> a reçu {"{:,}".format(int(montant-montant/10))} coins de <@{ctx.author.id}>")
                await ctx.reply(embed=embed)
            else:
                await ctx.reply("L'utilisateur n'a pas de profil.")
        else:
            await ctx.reply("Utilisateur invalide !")