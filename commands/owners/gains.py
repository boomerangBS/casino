# GAINS COMMANDS
# envoie les paramètres des gains
# setgains (setgain) : permet de modifier les paramètres des gains
# Permission requise : owner

import interactions
import asyncio
from interactions import Extension, Button, ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console



class SetGains(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command(aliases=["setgain"])
    async def setgains(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            console.log(f"setgains | {ctx.author} ({ctx.author.id})")
            while True:
                ctoken = self.bot.bdd.get_tokens_settings()[0]
                embed = interactions.Embed(description=f"**Gains** \n **Statut** : `{ctoken['status']}` \n **Gain** : `{ctoken['status_count']}` jeton(s) \n \n **Messages** : `{ctoken['messages']}` \n **Gain** : 1 jeton(s) \n \n **Heures de vocal** : `{ctoken['voice_hours']}` \n **Gain** : 1 jeton(s)")
                buttons = [Button(style=ButtonStyle.PRIMARY, label="Statut", custom_id="statut"), Button(style=ButtonStyle.PRIMARY, label="Messages", custom_id="messages"), Button(style=ButtonStyle.PRIMARY, label="Vocal", custom_id="vocal")]
                if "m" in locals():
                    await m.edit(embed=embed, components=[buttons])
                else:
                    m = await ctx.send(embed=embed, components=[buttons])
                try:
                    interaction = await self.bot.wait_for_component(components=buttons, timeout=100, check=lambda i: i.ctx.author == ctx.author and i.ctx.message == m)
                except asyncio.TimeoutError:
                    await m.edit(embed=embed, components=[])
                    await ctx.send("Temps écoulé.")
                    return
                interaction = interaction.ctx

                if interaction.custom_id == "statut":
                    first = await interaction.send("Veuillez envoyer le nouveau statut pour lequel les gains sont attribués.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé.")
                        continue
                    self.bot.bdd.set_tokens_settings("status", msg.message.content)
                    await ctx.send("Le statut pour lequel les gains sont attribués a été changé.")
                    await first.delete()
                    await msg.message.delete()
                    continue

                elif interaction.custom_id == "messages":
                    first = await interaction.send("Veuillez envoyer le nouveau nombre de messages qu'il faudra envoyer pour obtenir un jeton.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé.")
                        continue
                    try:
                        value = int(msg.message.content)
                    except:
                        await ctx.send("Veuillez envoyer un nombre valide.")
                        continue
                    self.bot.bdd.set_tokens_settings("messages", value)
                    await ctx.send("Le nombre de messages pour obtenir un jeton a été changé.")
                    await first.delete()
                    await msg.message.delete()
                    continue

                elif interaction.custom_id == "vocal":
                    first = await interaction.send("Veuillez envoyer le nouveau nombre d'heures qu'il faudra passer en vocal pour obtenir un jeton.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé.")
                        continue
                    try:
                        value = int(msg.message.content)
                    except:
                        await ctx.send("Veuillez envoyer un nombre valide.")
                        continue
                    self.bot.bdd.set_tokens_settings("voice_hours", value)
                    await ctx.send("Le nombre d'heures pour obtenir un jeton en vocal a été changé.")
                    await first.delete()
                    await msg.message.delete()
                    continue
