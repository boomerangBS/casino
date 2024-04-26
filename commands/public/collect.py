# COLLECT COMMAND
# collect donne entre 0 et 2000 toutes les 20 minutes

import random,interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console,generate_log_embed
from datetime import datetime, timedelta

class Collect(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def collect(self, ctx):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    await ctx.reply("Cette commande n'est pas autorisée dans ce salon !")
                    return
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
                embed=interactions.Embed(title=":coin: Collect",description=f"Vous avez obtenu {"{:,}".format(coins)} coins !")
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a collecté {"{:,}".format(coins)} coins")
                await ctx.reply(embed=embed)
                t = datetime.now()
                t = datetime.strftime(t,"%Y-%m-%d %H:%M:%S")
                bdd.set_countdown(ctx.author.id,"collect",t)
            else:
                time_left = timedelta(minutes=20) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.reply(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser cette commande !")