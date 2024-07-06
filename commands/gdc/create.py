import interactions,random,asyncio
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console,generate_log_embed
from datetime import datetime,timedelta
# ! NE PAS OUBLIER : CHECK SI LE JOUEUR EST DANS UN CLAN (NON OWNER)
class Create(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def create(self, ctx):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
        bdd=self.bot.bdd
        status=bdd.get_gamedata("gdc","status")
        channel=bdd.get_gamedata("gdc","channel")
        if status == []:
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if status[0]["datavalue"] == "off":
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if channel == []:
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if channel[0]["datavalue"] == "NO":
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if ctx.channel.id != int(channel[0]["datavalue"]):
            await ctx.reply(f"Cette commande est uniquement utilisable dans <#{channel[0]["datavalue"]}>")
            return
        u=bdd.check_user(ctx.author.id)
        if u == []:
            return
        u=u[0]
        if u["clan"] != None:
            if u["clan"] != "":
                await ctx.reply("Vous êtes déjà dans un clan !")
                return
        if u["coins"] < 5000:
            await ctx.reply("Il vous faut 5,000 coins pour pouvoir créer un clan !")
            return
        msg = await ctx.reply("Veuillez entrer le nom de votre clan.")
        def check(m):
            return m.message.author == ctx.author and m.message.channel == ctx.channel
        try:
            name = await self.bot.wait_for("message_create", checks=check, timeout=60)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(content="Temps écoulé.")
            return
        await msg.delete()
        await name.message.delete()
        name=name.message
        if len(name.content) > 20:
            await ctx.send(content="Le nom de votre clan ne doit pas dépasser 20 caractères.")
            return
        if len(name.content) < 3:
            await ctx.send(content="Le nom de votre clan doit contenir au moins 3 caractères.")
            return
        u=bdd.check_user(ctx.author.id)[0]
        id=bdd.add_clan(name.content,"Bienvenue dans votre clan.",ctx.author.id)
        bdd.set_coins(u["coins"]-5000,ctx.author.id)
        bdd.set_clan(id,ctx.author.id)
        await ctx.send(f"Votre clan **{name.content}** a été créé avec succès !")
        console.log(f"create | {ctx.author} ({ctx.author.id})")
        await generate_log_embed(self.bot,f"{ctx.author.mention} a créé le clan {name.content} pour 5,000 coins.")
        
        
