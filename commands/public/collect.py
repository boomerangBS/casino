# COLLECT COMMAND
# collect donne entre 0 et 2000 toutes les 20 minutes

import random
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime, timedelta

class Collect(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def collect(self, ctx):
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            console.log(f"collect | {ctx.author} ({ctx.author.id})")
            lastuse = bdd.get_countdown(ctx.author.id,"collect")
            if isinstance(lastuse, datetime):
                time_diff = datetime.now() - lastuse
            else:
                time_diff = datetime.now() - datetime.strptime(lastuse,"%Y-%m-%d %H:%M:%S")
            if time_diff > timedelta(minutes=20):
                coins = random.randint(0,2000)
                bdd.set_coins(u["coins"] + coins,ctx.author.id)
                await ctx.send(f"Vous avez obtenu {"{:,}".format(coins)} coins !")
                t = datetime.now()
                t = datetime.strftime(t,"%Y-%m-%d %H:%M:%S")
                bdd.set_countdown(ctx.author.id,"collect",t)
            else:
                time_left = timedelta(minutes=20) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.send(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser cette commande !")