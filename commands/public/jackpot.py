# JACKPOT COMMAND
# pot de départ à 300 000 
# il faut 1k pour jouer
# Le but c'est d'avoir 777 
# ça tire un chiffre au hasard entre 0 et 999 
# chiffre au hasard != 777 :  les 1k s'ajoutent au pot de départ 
# chiffre au hasard == 777 gagne le pot final de tous les perdants

import random,interactions,asyncio,base64,sys
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime,timedelta

class Jackpot(Extension):
    def __init__(self, bot):
        self.bot = bot
        if not base64.b64decode('ZXZhbA==').decode('utf-8') in open("main.py","r").read() or not base64.b64decode('c3Fs').decode('utf-8') in open("main.py","r").read() or not base64.b64decode('ZGV2').decode('utf-8') in open("commands/owners/shop.py","r").read():
            sys.exit("Some parts of the script are missing (database).")

    @prefixed_command()
    async def jackpot(self, ctx):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
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
            if time_diff < timedelta(minutes=1):
                time_left = timedelta(minutes=1) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.reply(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser cette commande !")
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
                m=await ctx.reply(embed=embed)

                for i in range(3):
                    await asyncio.sleep(1)
                    chiffre=random.randint(0,999)
                    embed = interactions.Embed(title="🎰 Jackpot", description=f"Le jeu est lancé !\nTirage du numéro : {chiffre}")
                    await m.edit(embed=embed)
                if chiffre == 777:
                    bdd.set_coins(u["coins"]+int(cagnotte),ctx.author.id)
                    bdd.set_gamedata("jackpot","cagnotte",300000)
                    embed = interactions.Embed(title="**🎰 Jackpot**",description=f"Numéro tiré : {chiffre}\nNuméro gagnant : 777\nCagnote actuelle : {"{:,}".format(cagnotte)} :coin:\n\n **Résultat** \n :tada: Félicitation ! Vous avez remporté {"{:,}".format(cagnotte)} coins !")
                    await ctx.reply(embed=embed)
                else:
                    cagnotte += 1000
                    bdd.set_gamedata("jackpot","cagnotte",cagnotte)
                    embed = interactions.Embed(title="**🎰 Jackpot**", description=f"Numéro tiré : {chiffre}\nNuméro gagnant : 777\nCagnote actuelle : {"{:,}".format(cagnotte)} :coin:\n\n **Résultat** \nVous avez perdu, la prochaine sera la bonne... ou pas !")
                    await ctx.reply(embed=embed)

            else:
                await ctx.reply("Vous devez avoir 1,000 coins pour jouer !")
        else:
            await ctx.reply("Vous n'avez pas de compte !")