#COMMAND RANK
#affiche le top des members ayant le plus de points

import interactions,random
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console


class Rank(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def rank(self, ctx):
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