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
                embed = interactions.Embed(title="🎰 Jackpot", description=str(cagnotte))
                m=await ctx.reply(embed=embed)
                await asyncio.sleep(5)
                chiffre = random.randint(0,999)
                if chiffre == 777:
                    bdd.set_coins(u["coins"]+int(cagnotte),ctx.author.id)
                    bdd.set_gamedata("jackpot","cagnotte",300000)
                    await m.edit(content=f"Vous avez obtenu {chiffre} !",embed=None)
                    await ctx.send(f"{ctx.author.mention} 🎉 Bravo ! Vous avez gagné le jackpot de {cagnotte} coins !")
                else:
                    cagnotte += 1000
                    bdd.set_gamedata("jackpot","cagnotte",cagnotte)
                    await m.edit(content=f"Vous avez obtenu {chiffre} !",embed=None)
                    await ctx.send(f"{ctx.author.mention} Vous avez perdu ! La cagnotte est maintenant de {cagnotte} coins !")

            else:
                await ctx.send("Vous n'avez pas assez de coins pour jouer !")
        else:
            await ctx.send("Vous n'avez pas de compte !")