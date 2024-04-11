# COMMANDE TOP
# Description: Affiche le top des membres ayant le plus de coins
#top

import interactions,random
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime,timedelta

class Top(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def top(self, ctx):
        bdd=self.bot.bdd
        users = bdd.list_users()
        if users == []:
            await ctx.send("Aucun utilisateur n'est inscrit sur le bot !")
            return
        users = sorted(users, key=lambda x: x["coins"], reverse=True)
        description="Voici le classement des utilisateurs les plus riches du serveur."
        for i in range(10):
            try:
                user = users[i]
                if i+1 == 1:
                    description += f"\n\n🥇 <@{user['id']}> - {"{:,}".format(user['coins'])} :coin:"
                elif i+1 == 2:
                    description += f"\n🥈 <@{user['id']}> - {"{:,}".format(user['coins'])} :coin:"
                elif i+1 == 3:
                    description += f"\n🥉 <@{user['id']}> - {"{:,}".format(user['coins'])} :coin:"
                else:
                    description += f"\n{i+1}. <@{user['id']}> - {u"{:,}".format(user['coins'])} :coin:"
            except:
                break
        embed = interactions.Embed(title="🏆 Leaderboard",description=description)
        embed.set_footer(text=self.bot.config["footer"])
        await ctx.send(embed=embed)