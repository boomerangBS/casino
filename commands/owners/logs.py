# SETLOGS COMMAND
# Permet de définir les logs

#permissions requises : owner

import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from datetime import datetime
from utils import console

class Setlogs(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def setlogs(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            while True:
                bdd=self.bot.bdd
                logs=bdd.get_gamedata("logs","channel")
                if logs == []:
                    bdd.add_gamedata("logs","channel","NO")
                    logs=bdd.get_gamedata("logs","channel")
                if logs[0]["datavalue"] == "NO":
                    logs = "Non défini"
                else:
                    logs = f"<#{logs[0]['datavalue']}>"
                embed = interactions.Embed(title="Logs",description=f"Salon : {logs}")
                buttons=[]
                buttons.append(Button(style=ButtonStyle.PRIMARY,label="Salon",custom_id="logs_channel"))
                if "m" in locals():
                    await m.edit(embed=embed,components=[buttons])
                else:
                    m=await ctx.send(embed=embed,components=[buttons])
                try:
                    i=await self.bot.wait_for_component(components=buttons,timeout=60,check=lambda i: i.ctx.author.id == ctx.author.id and i.ctx.message.id == m.id)
                except:
                    await m.edit(components=[])
                    continue
                if i.ctx.custom_id == "logs_channel":
                    await m.edit(components=[])
                    a=await i.ctx.send("Veuillez mentionner le salon de logs.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        data = await self.bot.wait_for('message_create', checks=check, timeout=50)
                        await data.message.delete()
                        data = data.message.content
                        await a.delete()
                        try:
                            data = int(data)
                            r = ctx.guild.get_channel(data)
                            if r is None:
                                await ctx.send("Ce salon n'existe pas !")
                                continue
                        except:
                            try:
                                data = data.split("<#")[1].split(">")[0]
                            except:
                                await ctx.send("Veuillez entrer un salon valide !")
                                continue
                            r = ctx.guild.get_channel(int(data))
                            if r is None:
                                await ctx.send("Ce salon n'existe pas !")
                                continue
                    except:
                        await ctx.send("Temps écoulé.")
                        continue
                    bdd.set_gamedata("logs","channel",data)
                    await ctx.send("Salon de logs défini.")
                    continue
                else:
                    continue
            return
        else:
            await ctx.send("Vous n'avez pas les permissions pour effectuer cette commande.")
            return
