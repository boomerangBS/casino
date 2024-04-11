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
        if chiffre == None:
            await ctx.send("Vous devez choisir un chiffre entre 0 et 999 !")
            return
        if chiffre < 0 or chiffre > 999:
            await ctx.send("Vous devez choisir un chiffre entre 0 et 999 !")
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
            if time_diff < timedelta(minutes=2):
                time_left = timedelta(minutes=2) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.send(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser a nouveau cette commande !")
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
                m=await ctx.send(embed=embed)

                for i in range(3):
                    await asyncio.sleep(1)
                    chiffre_aleatoire=random.randint(0,999)
                    embed = interactions.Embed(title="🎰 Bingo", description=f"Le jeu est lancé !\nTirage du numéro : {chiffre_aleatoire}")
                    await m.edit(embed=embed)
                if chiffre_aleatoire == chiffre:
                    bdd.set_coins(u["coins"]+int(cagnotte),ctx.author.id)
                    bdd.set_gamedata("bingo","cagnotte",10000)
                    embed = interactions.Embed(title="**🎰 Bingo**",description=f"Numéro tiré : {chiffre_aleatoire}\nNuméro gagnant : {chiffre}\nCagnote actuelle : {cagnotte} :coin:\n\n**:tada: Félicitation ! Vous avez remporté {cagnotte} coins ! **")
                    await ctx.reply(embed=embed)
                else:
                    cagnotte += 250
                    bdd.set_gamedata("bingo","cagnotte",cagnotte)
                    embed = interactions.Embed(title="**🎰 Bingo**", description=f"Numéro tiré : {chiffre_aleatoire}\nNuméro gagnant : {chiffre}\nCagnote actuelle : {cagnotte} :coin:\n\n**Vous avez perdu, la prochaine sera la bonne... ou pas !**")
                    await ctx.reply(embed=embed)
            else:
                await ctx.send("Vous n'avez pas assez de coins pour jouer !")
