# RESET COMMAND
# Permet de reset le bot

#permissions requises : owner

import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from datetime import datetime
from utils import console

class Reset(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def reset(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            embed = interactions.Embed(title="Reset",description=":warning: Êtes-vous sûr de vouloir reset ? Cette action est irréversible.")
            buttons=[]
            buttons.append(Button(style=ButtonStyle.DANGER,label="All",custom_id="reset"))
            buttons.append(Button(style=ButtonStyle.SECONDARY,label="Coins",custom_id="coins"))
            buttons.append(Button(style=ButtonStyle.SECONDARY,label="Jetons",custom_id="tokens"))
            buttons.append(Button(style=ButtonStyle.SECONDARY,label="Roulette & shop",custom_id="rs"))
            buttons.append(Button(style=ButtonStyle.SECONDARY,label="GDC",custom_id="gdc"))
            m=await ctx.reply(embed=embed,components=[buttons])
            console.log(f"reset | {ctx.author} ({ctx.author.id})")
            try:
                i=await self.bot.wait_for_component(components=buttons,timeout=60,check=lambda i: i.ctx.author.id == ctx.author.id and i.ctx.message.id == m.id)
                await m.edit(components=[])
                if i.ctx.custom_id == "reset":
                    mm=await ctx.send("Êtes-vous **vraiment** sûr de vouloir **reset le bot** ? Si oui, envoyez `oui, reset ce bot`.")
                    def check(m):
                        return m.message.author == ctx.author and m.message.channel == ctx.channel
                    try:
                        data = await self.bot.wait_for('message_create', checks=check, timeout=50)
                        await data.message.delete()
                        data = data.message.content
                        await mm.delete()
                        if data == "oui, reset ce bot" or data == "d":
                            await ctx.send("Reset en cours...")
                            self.bot.bdd.reset()
                            await ctx.send("Reset effectué ! Veuillez effectuer la commande panel pour reconfigurer le bot (redemarage du bot conseillé).")
                        else:
                            await ctx.send("Reset annulé.")
                    except:
                        await ctx.send("Reset annulé (1).")
                elif i.ctx.custom_id == "coins":
                    await ctx.send("Reset en cours...")
                    self.bot.bdd.query("UPDATE profiles SET coins=0 WHERE 1=1")
                    await ctx.send("Reset effectué !")
                elif i.ctx.custom_id == "pillages":
                    await ctx.send("Reset en cours...")
                    self.bot.bdd.query("UPDATE profiles SET rob_availables=0 WHERE 1=1")
                    await ctx.send("Reset effectué !")
                elif i.ctx.custom_id == "tokens":
                    await ctx.send("Reset en cours...")
                    self.bot.bdd.query("UPDATE profiles SET tokens=0 WHERE 1=1")
                    await ctx.send("Reset effectué !")
                elif i.ctx.custom_id == "rs":
                    await ctx.send("Reset en cours...")
                    self.bot.bdd.query("DELETE FROM roulette_items")
                    self.bot.bdd.query("DELETE FROM roulette_category")
                    self.bot.bdd.query("DELETE FROM shop")
                    await ctx.send("Reset effectué !")
                elif i.ctx.custom_id == "gdc":
                    await ctx.send("Reset en cours...")
                    self.bot.bdd.query("UPDATE profiles SET clan='' WHERE 1=1")
                    await ctx.send("Reset effectué !")

            except Exception as e:
                await m.edit(components=[])
                await ctx.send(f"Reset annulé (2). {e}")
                return