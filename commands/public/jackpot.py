# JACKPOT COMMAND
# pot de départ à 300 000 
# il faut 1k pour jouer
# Le but c'est d'avoir 777 
# ça tire un chiffre au hasard entre 0 et 999 
# chiffre au hasard != 777 :  les 1k s'ajoutent au pot de départ 
# chiffre au hasard == 777 gagne le pot final de tous les perdants

import random,interactions,asyncio
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime,timedelta

class Jackpot(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def jackpot(self, ctx):
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            console.log(f"jackpot | {ctx.author} ({ctx.author.id})")
            lastuse = bdd.get_countdown(ctx.author.id,"jackpot")
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
            bdd.set_countdown(ctx.author.id,"jackpot",now)
            if u["coins"] >= 1000:
                coins = u["coins"] - 1000
                bdd.set_coins(coins,ctx.author.id)
                cagnotte = bdd.get_gamedata("jackpot","cagnotte")
                if cagnotte == []:
                    cagnotte = 300000
                    bdd.add_gamedata("jackpot","cagnotte",cagnotte)
                else:
                    cagnotte = cagnotte[0]["datavalue"]
                    bdd.set_gamedata("jackpot","cagnotte",cagnotte+1000)
                embed = interactions.Embed(title="🎰 Jackpot", description="Le jeu est lancé !")
                m=await ctx.send(embed=embed)

                for i in range(3):
                    await asyncio.sleep(1)
                    chiffre=random.randint(0,999)
                    embed = interactions.Embed(title="🎰 Jackpot", description=f"Le jeu est lancé !\nTirage du numéro : {chiffre}")
                    await m.edit(embed=embed)
                if chiffre == 777:
                    bdd.set_coins(u["coins"]+int(cagnotte),ctx.author.id)
                    bdd.set_gamedata("jackpot","cagnotte",300000)
                    embed = interactions.Embed(title="**🎰 Jackpot**",description=f"Numéro tiré : {chiffre}\nNuméro gagnant : 777\nCagnote actuelle : {cagnotte} :coin:\n\n**:tada: Félicitation ! Vous avez remporté {cagnotte} coins ! **")
                    await ctx.reply(embed=embed)
                else:
                    cagnotte += 1000
                    bdd.set_gamedata("jackpot","cagnotte",cagnotte)
                    embed = interactions.Embed(title="**🎰 Jackpot**", description=f"Numéro tiré : {chiffre}\nNuméro gagnant : 777\nCagnote actuelle : {cagnotte} :coin:\n\n**Vous avez perdu, la prochaine sera la bonne... ou pas !**")
                    await ctx.reply(embed=embed)

            else:
                await ctx.send("Vous n'avez pas assez de coins pour jouer !")
        else:
            await ctx.send("Vous n'avez pas de compte !")