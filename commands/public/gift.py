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
            console.log(f"gift | {ctx.author} ({ctx.author.id})")
            lastuse = bdd.get_countdown(ctx.author.id,"gift")
            if isinstance(lastuse, datetime):
                time_diff = datetime.now() - lastuse
            else:
                time_diff = datetime.now() - datetime.strptime(lastuse,"%Y-%m-%d %H:%M:%S")
            if time_diff > timedelta(minutes=20):
                embed = interactions.Embed(title="🎁 Cadeau", description="Cliquez sur un des trois cadeaux pour obtenir entre 0 et 5,000 coins !")
                buttons=[Button(style=ButtonStyle.BLUE, label="🎁", custom_id="1"),Button(style=ButtonStyle.GREEN, label="🎁", custom_id="2"),Button(style=ButtonStyle.RED, label="🎁", custom_id="3")]
                first=await ctx.reply(embed=embed, components=[buttons])
                try:
                    i = await self.bot.wait_for_component(components=buttons, timeout=100,check=lambda i: i.ctx.author == ctx.author and i.ctx.message == first)
                except asyncio.TimeoutError:
                    await first.edit(components=[])
                    return
                t = datetime.now()
                t = datetime.strftime(t,"%Y-%m-%d %H:%M:%S")
                bdd.set_countdown(ctx.author.id,"gift",t)
                await first.edit(components=[])
                choice = random.randint(1,3)
                if int(i.ctx.custom_id) == choice:
                    coins = random.randint(0,5000)
                    bdd.set_coins(u["coins"] + coins,ctx.author.id)
                    embed = interactions.Embed(title="🎁 Cadeau", description=f"Bravo ! Vous avez gagné {"{:,}".format(coins)} coins !")
                    await i.ctx.edit_origin(embed=embed)
                else:
                    embed = interactions.Embed(title="🎁 Cadeau", description=f"Vous avez perdu !")
                    await i.ctx.edit_origin(embed=embed)
            else:
                time_left = timedelta(minutes=20) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.reply(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser cette commande !")
