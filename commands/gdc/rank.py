#COMMAND RANK
#affiche le top des members ayant le plus de points

import interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command


class Rank(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def rank(self, ctx):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
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
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
        bdd=self.bot.bdd
        users = bdd.list_users()
        if users == []:
            await ctx.reply("Aucun utilisateur n'est inscrit sur le bot !")
            return
        users = sorted(users, key=lambda x: x["points"], reverse=True)
        description="Voici le classement des utilisateurs ayant le plus de points."
        for i in range(10):
            try:
                user = users[i]
                if i+1 == 1:
                    description += f"\n\n🥇 <@{user['id']}> - {"{:,}".format(user['points'])} :star:"
                elif i+1 == 2:
                    description += f"\n🥈 <@{user['id']}> - {"{:,}".format(user['points'])} :star:"
                elif i+1 == 3:
                    description += f"\n🥉 <@{user['id']}> - {"{:,}".format(user['points'])} :star:"
                else:
                    description += f"\n{i+1}. <@{user['id']}> - {u"{:,}".format(user['points'])} :star:"
            except:
                break
        embed = interactions.Embed(title="🏆 Leaderboard",description=description)
        embed.set_footer(text=self.bot.config["footer"])
        await ctx.reply(embed=embed)