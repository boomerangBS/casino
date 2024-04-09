# GAINS COMMANDS
# envoie les parametres des gains
#gainstatus : afficher la config actuelle pour le status
#gainstatus <status> : changer le status pour lequel les gains sont attribués
# Permission requise : owner

import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class SetGains(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def gains(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            console.log(f"setgains | {ctx.author} ({ctx.author.id})")
            ctoken = self.bot.bdd.get_tokens_settings()[0]
            elif sub == "status":
                if subsub is None:
                    embed = interactions.Embed(description=f"**Gain pour le status** \n **Status** : `{ctoken['status']}` \n **Gain** : `{ctoken['status_count']}` jeton(s)")
                    embed.set_footer(text="Pour changer le status ou le gain, utilisez ``setgains status <status/gain>``")
                    await ctx.send(embed=embed)
                    return
                
                elif subsub == "status":
                    await ctx.send("Veuillez envoyer le nouveau status pour lequel les gains sont attribués.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé.")
                        return
                    self.bot.bdd.set_tokens_settings("status",msg.message.content)
                    await ctx.send("Le status pour lequel les gains sont attribués a été changé.")
                    return
                
                elif subsub == "gain":
                    await ctx.send("Veuillez envoyer le nouveau nombre de jetons attribués.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé.")
                        return
                    try:
                        value=int(msg.message.content)
                    except:
                        await ctx.send("Veuillez envoyer un nombre valide.")
                        return
                    self.bot.bdd.set_tokens_settings("status_count",value)
                    await ctx.send("Le nombre de jetons attribués a été changé.")
                    return
                else:
                    await ctx.send("Veuiilez choisir un paramètre: ``status`` ou ``gain`` ou ne rien mettre")
                    return
                
            elif sub == "messages":
                if subsub is None:
                    embed = interactions.Embed(description=f"**Gain pour les messages** \n **Messages** : `{ctoken['messages']}` \n **Gain** : 1 jeton(s)")
                    embed.set_footer(text="Pour changer le nombre de messages, utilisez ``setgains messages <messages>``")
                    await ctx.send(embed=embed)
                    return
                
                elif subsub == "messages":
                    await ctx.send("Veuillez envoyer le nouveau nombre de messages qu'il faudrat envoyer pour obtenir un jeton.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé.")
                        return
                    try:
                        value=int(msg.message.content)
                    except:
                        await ctx.send("Veuillez envoyer un nombre valide.")
                        return
                    self.bot.bdd.set_tokens_settings("messages",value)
                    await ctx.send("Le nombre de messages pour obtenir un jeton a été changé.")
                    return
                else:
                    await ctx.send("Veuiilez choisir un paramètre: ``messages`` ou ne rien mettre")
                    return
                
            elif sub == "vocal":
                if subsub is None:
                    embed = interactions.Embed(description=f"**Gain pour les vocal** \n **Heures** : `{ctoken['voice_hours']}` \n **Gain** : 1 jeton(s)")
                    embed.set_footer(text="Pour changer le nombre d'heures, utilisez ``setgains vocal <heures>``")
                    await ctx.send(embed=embed)
                    return
                
                elif subsub == "heures":
                    await ctx.send("Veuillez envoyer le nouveau nombre d'heures qu'il faudrat passer en vocal pour obtenir un jeton.")
                    def check(m):
                        m = m.message
                        return m.author == ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.bot.wait_for('message_create', checks=check, timeout=50)
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé.")
                        return
                    try:
                        value=int(msg.message.content)
                    except:
                        await ctx.send("Veuillez envoyer un nombre valide.")
                        return
                    self.bot.bdd.set_tokens_settings("voice_hours",value)
                    await ctx.send("Le nombre d'heures' pour obtenir un jeton en vocal a été changé.")
                    return
                else:
                    await ctx.send("Veuiilez choisir un paramètre: ``heures`` ou ne rien mettre")
                    return