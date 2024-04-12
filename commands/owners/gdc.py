# GDC COMMAND
# Permet de lancer/stopper la guerre des clans

#permissions requises : owner

import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from datetime import datetime
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
                maxmembers=bdd.get_gamedata("gdc","maxmembers")
                duration=bdd.get_gamedata("gdc","duration")
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
                if maxmembers == []:
                    bdd.add_gamedata("gdc","maxmembers",3)
                    maxmembers=bdd.get_gamedata("gdc","maxmembers")
                if duration == []:
                    bdd.add_gamedata("gdc","duration",7)
                    duration=bdd.get_gamedata("gdc","duration")
                status = status[0]["datavalue"]
                embed = interactions.Embed(title="Guerre des clans",description=f"Statut : {status} \nSalon : {channel} \nNombre de membres par clan : {maxmembers[0]['datavalue']} \nDurée : {duration[0]['datavalue']} jours")
                buttons=[]
                if status == "on":
                    buttons.append(Button(style=ButtonStyle.DANGER,label="Arrêter",custom_id="gdc_off"))
                else:
                    buttons.append(Button(style=ButtonStyle.SUCCESS,label="Lancer",custom_id="gdc_on"))
                # buttons.append(Button(style=ButtonStyle.PRIMARY,label="Gains",custom_id="gdc_gains"))
                buttons.append(Button(style=ButtonStyle.PRIMARY,label="Salon",custom_id="gdc_channel"))
                buttons.append(Button(style=ButtonStyle.PRIMARY,label="Membres par clan",custom_id="gdc_members"))
                buttons.append(Button(style=ButtonStyle.PRIMARY,label="Durée",custom_id="gdc_duration"))
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
                        await i.send("Veuillez définir le salon de la guerre des clans avant de la lancer !")
                        continue
                    bdd.set_gamedata("gdc","status","on")
                    start = bdd.get_gamedata("gdc","start")
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if start == []:
                        bdd.add_gamedata("gdc","start",now)
                    else:
                        bdd.set_gamedata("gdc","start",now)
                    await i.send("La guerre des clans a été lancée !")
                    continue
                if i.custom_id == "gdc_off":
                    bdd.set_gamedata("gdc","status","off")
                    await i.send("La guerre des clans a été arrêtée !")
                    continue
                if i.custom_id == "gdc_channel":
                    ii=await i.send("Veuillez envoyer le salon de la guerre des clans.")
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
                if i.custom_id == "gdc_members":
                    ii=await i.send("Veuillez envoyer le nombre de membres par clan.")
                    def check(m):
                        return m.message.author.id == ctx.author.id and m.message.channel.id == ctx.channel.id
                    try:
                        members = await self.bot.wait_for("message_create",timeout=60,checks=check)
                        members=members.message
                    except asyncio.TimeoutError:
                        continue
                    try:
                        data = int(members.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre valide !")
                        continue
                    bdd.set_gamedata("gdc","maxmembers",data)
                    await ctx.send("Le nombre de membres par clan a bien été défini !")
                    await members.delete()
                    await ii.delete()
                    continue
                if i.custom_id == "gdc_duration":
                    ii=await i.send("Veuillez envoyer la durée de la guerre des clans.")
                    def check(m):
                        return m.message.author.id == ctx.author.id and m.message.channel.id == ctx.channel.id
                    try:
                        duration = await self.bot.wait_for("message_create",timeout=60,checks=check)
                        duration=duration.message
                    except asyncio.TimeoutError:
                        continue
                    try:
                        data = int(duration.content)
                    except:
                        await ctx.send("Veuillez entrer un nombre valide !")
                        continue
                    bdd.set_gamedata("gdc","duration",data)
                    await ctx.send("La durée de la guerre des clans a bien été définie !")
                    await duration.delete()
                    await ii.delete()
                    continue