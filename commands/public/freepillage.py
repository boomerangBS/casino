# FREEPILLAGE COMMAND
#ne require rien
# prend entre 0 et 3 jetons au joueur ciblé et les donne au joueurs attaquant
#pillage <user>
# countdown : 2h

import interactions,random
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime,timedelta

class Freepillage(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def freepillage(self, ctx, user=None):
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
        if user == None:
            await ctx.reply("Vous devez mentionner un utilisateur !")
            return
        try:
            user = int(user)
        except:
            try:
                user = int(user.split("<@")[1].split(">")[0])
            except:
                await ctx.reply("Utilisateur invalide !")
                return
        if user == ctx.author.id:
            await ctx.reply("Vous ne pouvez pas vous piller vous même !")
            return
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            console.log(f"freepillage | {ctx.author} ({ctx.author.id})")
            lastuse = bdd.get_countdown(ctx.author.id,"freepillage")
            if isinstance(lastuse, datetime):
                time_diff = datetime.now() - lastuse
            else:
                time_diff = datetime.now() - datetime.strptime(lastuse,"%Y-%m-%d %H:%M:%S")
            if time_diff < timedelta(hours=2):
                time_left = timedelta(hours=2) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.reply(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser cette commande !")
                return
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            target = bdd.check_user(user)
            if target == []:
                await ctx.reply("L'utilisateur n'a pas de profil. ")
                return
            target = target[0]
            r = random.randint(0,3)
            bdd.set_countdown(ctx.author.id,"freepillage",now)
            if r == 0:
                embed = interactions.Embed(title="Freepillage",description=f"Vous n'avez pas réussi a piller <@{user}> !")
                await ctx.reply(embed=embed)
            else:
                bdd.set_points(u["points"]+r,ctx.author.id)
                bdd.set_points(target["points"]-r,user)
                embed = interactions.Embed(title="Freepillage",description=f"Vous avez pillé {r} jetons à <@{user}> !")
                await ctx.reply(embed=embed)
                console.log(f"freepillage | {ctx.author} ({ctx.author.id}) a pillé {r} jetons à {user} ({user})")