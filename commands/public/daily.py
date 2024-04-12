# DAILY COMMAND
#daily donne entre 0 et 20000 coins toutes les 24h

import random,interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime, timedelta

class Daily(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def daily(self, ctx):
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            console.log(f"daily | {ctx.author} ({ctx.author.id})")
            lastuse = bdd.get_countdown(ctx.author.id,"daily")
            if isinstance(lastuse, datetime):
                time_diff = datetime.now() - lastuse
            else:
                time_diff = datetime.now() - datetime.strptime(lastuse,"%Y-%m-%d %H:%M:%S")
            if time_diff > timedelta(days=1):
                coins = random.randint(0,20000)
                bdd.set_coins(u["coins"] + coins,ctx.author.id)
                embed = interactions.Embed(title="Daily",description=f"Vous avez obtenu {"{:,}".format(coins)} coins !")
                await ctx.send(embed=embed)
                t = datetime.now()
                t = datetime.strftime(t,"%Y-%m-%d %H:%M:%S")
                bdd.set_countdown(ctx.author.id,"daily",t)
            else:
                time_left = timedelta(days=1) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.send(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser cette commande !")
