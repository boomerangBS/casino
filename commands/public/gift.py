import interactions,asyncio,random
from interactions import Extension
from interactions import Button, ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime, timedelta

class Gift(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def gift(self, ctx):
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            console.log(f"gift | {ctx.author} ({ctx.author.id})")
            lastuse = bdd.get_countdown(ctx.author.id,"gift")
            if isinstance(lastuse, datetime):
                time_diff = datetime.now() - lastuse
            else:
                time_diff = datetime.now() - datetime.strptime(lastuse,"%Y-%m-%d %H:%M:%S")
            if time_diff > timedelta(days=1):
                embed = interactions.Embed(title="🎁 Cadeau", description="Cliquez sur un des trois cadeaux pour obtenir entre 0 et 5000 coins !")
                buttons=[Button(style=ButtonStyle.BLUE, label="🎁", custom_id="1"),Button(style=ButtonStyle.GREEN, label="🎁", custom_id="2"),Button(style=ButtonStyle.RED, label="🎁", custom_id="3")]
                first=await ctx.reply(embed=embed, components=[buttons])
                try:
                    i = await self.bot.wait_for_component(components=buttons, timeout=100,check=lambda i: i.ctx.author == ctx.author and i.ctx.message == first)
                except asyncio.TimeoutError:
                    await ctx.send("Vous avez mis trop de temps à choisir un cadeau !")
                    await first.edit(components=[])
                    return
                bdd.set_countdown(ctx.author.id,"gift",t)
                await first.edit(components=[])
                choice = random.randint(1,3)
                if int(i.ctx.custom_id) == choice:
                    coins = random.randint(0,5000)
                    bdd.set_coins(u["coins"] + coins,ctx.author.id)
                    await i.ctx.send(f"Bravo ! Vous avez gagné {coins} coins !")
                else:
                    await i.ctx.send("Vous avez perdu !")
                t = datetime.now()
                t = datetime.strftime(t,"%Y-%m-%d %H:%M:%S")
            else:
                time_left = timedelta(days=1) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.send(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser a nouveau cette commande !")
