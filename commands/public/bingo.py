# Bingo COMMAND
# pot de départ à 10000
# il faut 250 pour jouer
# Le but c'est d'avoir un chiffre choisi par le joueur 
# ça tire un chiffre au hasard entre 0 et 999 
# chiffre au hasard != chiffree choisi par le joueur :  les 250 s'ajoutent au pot de départ 
# chiffre au hasard == chiffree choisi par le joueur gagne le pot final de tous les perdants
# countdown : 2 minutes

import random,interactions,asyncio
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime,timedelta

class Bingo(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def bingo(self, ctx, chiffre:int=None):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
            
        if chiffre == None:
            await ctx.reply("Vous devez choisir un chiffre entre 0 et 100 !")
            return
        if chiffre < 0 or chiffre > 100:
            await ctx.reply("Vous devez choisir un chiffre entre 0 et 100 !")
            return
        
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            console.log(f"bingo | {ctx.author} ({ctx.author.id})")
            lastuse = bdd.get_countdown(ctx.author.id,"bingo")
            if isinstance(lastuse, datetime):
                time_diff = datetime.now() - lastuse
            else:
                time_diff = datetime.now() - datetime.strptime(lastuse,"%Y-%m-%d %H:%M:%S")
            if time_diff < timedelta(minutes=1):
                time_left = timedelta(minutes=1) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.reply(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser cette commande !")
                return
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bdd.set_countdown(ctx.author.id,"bingo",now)
            if u["coins"] >= 250:
                coins = u["coins"] - 250
                bdd.set_coins(coins,ctx.author.id)
                cagnotte = bdd.get_gamedata("bingo","cagnotte")
                if cagnotte == []:
                    cagnotte = 10000
                    bdd.add_gamedata("bingo","cagnotte",cagnotte)
                else:
                    cagnotte = cagnotte[0]["datavalue"]
                    bdd.set_gamedata("bingo","cagnotte",cagnotte+250)

                embed = interactions.Embed(title="🎰 Bingo", description="Le jeu est lancé !")
                m=await ctx.reply(embed=embed)

                for i in range(3):
                    await asyncio.sleep(1)
                    chiffre_aleatoire=random.randint(0,100)
                    embed = interactions.Embed(title="🎰 Bingo", description=f"Le jeu est lancé !\nTirage du numéro : {chiffre_aleatoire}")
                    await m.edit(embed=embed)
                if chiffre_aleatoire == chiffre:
                    bdd.set_coins(u["coins"]+int(cagnotte),ctx.author.id)
                    bdd.set_gamedata("bingo","cagnotte",10000)
                    embed = interactions.Embed(title="**🎰 Bingo**",description=f"Numéro choisi : {chiffre}\nNuméro gagnant : {chiffre_aleatoire}\nCagnote actuelle : {"{:,}".format(cagnotte)} :coin:\n\n **Résultat** \n:tada: Félicitation ! Vous avez remporté {"{:,}".format(cagnotte)} coins !")
                    await ctx.reply(embed=embed)
                else:
                    cagnotte += 250
                    bdd.set_gamedata("bingo","cagnotte",cagnotte)
                    embed = interactions.Embed(title="**🎰 Bingo**", description=f"Numéro choisi : {chiffre}\nNuméro gagnant : {chiffre_aleatoire}\nCagnote actuelle : {"{:,}".format(cagnotte)} :coin:\n\n **Résultat** \nVous avez perdu, la prochaine sera la bonne... ou pas !")
                    await ctx.reply(embed=embed)
            else:
                await ctx.reply("Vous devez avoir 250 coins pour jouer !")
