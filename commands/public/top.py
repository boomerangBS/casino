# COMMANDE TOP
# Description: Affiche le top des membres ayant le plus de coins
#top

import interactions,random,math
from interactions import Extension,Button,ButtonStyle
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
            await ctx.reply("Aucun utilisateur n'est inscrit sur le bot !")
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
        i=1
        maxpages = math.ceil(len(users) / 10)
        arrows = [Button(style=ButtonStyle.PRIMARY, label="◀️", custom_id="prev"), Button(style=ButtonStyle.PRIMARY, label="▶️", custom_id="next")]
        c=await ctx.reply(embed=embed,components=[arrows])
        try:
            iii=await self.bot.wait_for_component(components=arrows,timeout=200,check=lambda iii: iii.ctx.author.id == ctx.author.id and iii.ctx.message.id == c.id)
        except:
            await c.edit(components=[])
        if iii.ctx.custom_id == "prev":
            if i == 1:
                i = 1
            else:
                i -= 1
        else:
            if i == maxpages:
                i = 1
            else:
                i += 1
        description="Voici le classement des utilisateurs les plus riches du serveur."
        for ii in range(10):
            try:
                if i == 1:
                    user = users[i]
                    if ii+1 == 1:
                        description += f"\n\n🥇 <@{user['id']}> - {"{:,}".format(user['coins'])} :coin:"
                    elif ii+1 == 2:
                        description += f"\n🥈 <@{user['id']}> - {"{:,}".format(user['coins'])} :coin:"
                    elif ii+1 == 3:
                        description += f"\n🥉 <@{user['id']}> - {"{:,}".format(user['coins'])} :coin:"
                    else:
                        description += f"\n{ii+1}. <@{user['id']}> - {u"{:,}".format(user['coins'])} :coin:"
                else:
                    user = users[ii+i+1*10]
                    description += f"\n{ii+1+i*10}. <@{user['id']}> - {u"{:,}".format(user['coins'])} :coin:"
                await c.edit(embed=embed,components=[arrows])
            except:
                break