# ROB COMMAND
#requiert 1 pillage dans son compte
# prend entre 0 et 10000 coins au joueur ciblé et les donne au joueurs attaquant
#rob <user>
# countdown : 20mn

import interactions,random
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console,generate_log_embed
from datetime import datetime,timedelta

class Rob(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def rob(self, ctx, user=None):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
        bdd=self.bot.bdd
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
            if u["rob_availables"] < 1:
                await ctx.reply("Vous n'avez pas de pillages disponibles !")
                return
            console.log(f"rob | {ctx.author} ({ctx.author.id})")
            lastuse = bdd.get_countdown(ctx.author.id,"rob")
            if isinstance(lastuse, datetime):
                time_diff = datetime.now() - lastuse
            else:
                time_diff = datetime.now() - datetime.strptime(lastuse,"%Y-%m-%d %H:%M:%S")
            if time_diff < timedelta(minutes=20):
                time_left = timedelta(minutes=20) - time_diff
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.reply(f":clock11: Vous devez attendre {hours} heures, {minutes} minutes et {seconds} secondes avant de pouvoir utiliser cette commande !")
                return
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            u2 = bdd.check_user(user)
            if u2 != []:
                u2 = u2[0]
                if u2["coins"] == 0:
                    embed = interactions.Embed(title=":knife: Rob",description=f"<@{user}> n'a pas de coins à voler !")
                    await ctx.reply(embed=embed)
                    return
                if u2["coins"] > 10000:
                    coins = random.randint(0,10000)
                else:
                    coins = random.randint(0,u2["coins"])
                bdd.set_pillages(u["rob_availables"]-1,ctx.author.id)
                bdd.set_countdown(ctx.author.id,"rob",now)
                bdd.set_coins(u["coins"]+coins,ctx.author.id)
                bdd.set_coins(u2["coins"]-coins,user)
                embed= interactions.Embed(title=":knife: Rob",description=f"Vous avez volé {"{:,}".format(coins)} coins à <@{user}> !")
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a volé {"{:,}".format(coins)} coins à <@{user}>")
                await ctx.reply(embed=embed)
            else:
                await ctx.reply("L'utilisateur n'a pas de profil. ")
