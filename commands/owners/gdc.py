# GDC COMMAND
# Permet de lancer/stopper la guerre des clans

#permissions requises : owner

import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class Gdc(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def setgdc(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            while True:
                bdd=self.bot.bdd
                status=bdd.get_gamedata("gdc","status")
                channel=bdd.get_gamedata("gdc","channel")
                if status == []:
                    bdd.add_gamedata("gdc","status","off")
                    status=bdd.get_gamedata("gdc","status")
                if channel == []:
                    bdd.add_gamedata("gdc","channel","NO")
                    channel=bdd.get_gamedata("gdc","channel")
                if channel[0]["datavalue"] == "NO":
                    channel = "Non défini"
                else:
                    channel = f"<#{channel[0]['datavalue']}>"
                status = status[0]["datavalue"]
                embed = interactions.Embed(description=f"**Guerre des clans**\n\nStatus : {status} \nSalon : {channel}")
                buttons=[]
                if status == "on":
                    buttons.append(Button(style=ButtonStyle.DANGER,label="Arrêter",custom_id="gdc_off"))
                else:
                    buttons.append(Button(style=ButtonStyle.SUCCESS,label="Lancer",custom_id="gdc_on"))
                buttons.append(Button(style=ButtonStyle.PRIMARY,label="Définir le salon",custom_id="gdc_channel"))
                if "m" in locals():
                    await m.edit(embed=embed,components=[buttons])
                else:
                    m=await ctx.send(embed=embed,components=[buttons])
                try:
                    i=await self.bot.wait_for_component(components=buttons,timeout=60,check=lambda i: i.ctx.author.id == ctx.author.id and i.ctx.message.id == m.id)
                except:
                    await m.edit(components=[])
                    continue
                i=i.ctx
                if i.custom_id == "gdc_on":
                    channel = bdd.get_gamedata("gdc","channel")
                    if channel[0]["datavalue"] == "NO":
                        await i.send("Vueillez définir le salon de la guerre des clans avant de la lancer !")
                        continue
                    bdd.set_gamedata("gdc","status","on")
                    await i.send("La guerre des clans a été lancée !")
                    continue
                if i.custom_id == "gdc_off":
                    bdd.set_gamedata("gdc","status","off")
                    await i.send("La guerre des clans a été arrêtée !")
                    continue
                if i.custom_id == "gdc_channel":
                    ii=await i.send("Veuillez mentionner le salon de la guerre des clans")
                    def check(m):
                        return m.message.author.id == ctx.author.id and m.message.channel.id == ctx.channel.id
                    try:
                        channel = await self.bot.wait_for("message_create",timeout=60,checks=check)
                        channel=channel.message
                    except asyncio.TimeoutError:
                        continue
                    try:
                        data = int(channel.content)
                        r = ctx.guild.get_channel(data)
                        if r is None:
                            await ctx.send("Ce salon n'existe pas !")
                            continue
                    except:
                        try:
                            data = channel.content.split("<#")[1].split(">")[0]
                        except:
                            await ctx.send("Veuillez entrer un salon valide !")
                            continue
                        r = ctx.guild.get_channel(int(data))
                        if r is None:
                            await ctx.send("Ce salon n'existe pas !")
                            continue
                    bdd.set_gamedata("gdc","channel",data)
                    await ctx.send("Le salon de la guerre des clans a bien été défini !")
                    await channel.delete()
                    await ii.delete()
                    continue