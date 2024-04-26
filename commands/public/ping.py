import time
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
class Ping(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def ping(self, ctx):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
        latency = self.bot.latency * 1000  # Convert to milliseconds
        if latency < 100:
            status = "Excellent"
        elif latency < 200:
            status = "Correct"
        elif latency < 300:
            status = "Moyen"
        else:
            status = "Nul !"

        m=await ctx.reply('Pong! Latence en cours de calcul...')
        start = time.monotonic()
        await m.edit(content="Latence d'edit en calcul")
        end = time.monotonic()
        edit_latency = (end - start) * 1000
        if edit_latency < 100:
            statuss = "Excellent"
        elif edit_latency < 200:
            statuss = "Correct"
        elif edit_latency < 300:
            statuss = "Moyen"
        else:
            statuss = "Nul !"
        await m.edit(content=f'Pong! Latence: {latency}ms ({status}) \nLatence d\'edit : {edit_latency}ms ({statuss})')
        console.log(f"ping | {ctx.author} ({ctx.author.id})| {latency}ms ({status}) | {edit_latency}ms ({statuss})")
        
