import interactions, random, asyncio
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console,generate_log_embed
isrool=[]
class roulette(Extension):
    def __init__(self, bot):
        self.bot = bot
    
    @prefixed_command(aliases=["rool","rl","rools"])
    async def roulette(self,ctx,case=None,mise=None):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
        u = self.bot.bdd.check_user(ctx.author.id)
        if u == []:
            return
        u = u[0]
        console.log(f"roulette | {ctx.author} ({ctx.author.id})")
        if case == None:
            await ctx.reply("Vous devez choisir une case ! `pair`x2 `impair`x2 `rouge`x2 `noir`x2 `vert`x12 `1-36`x12")
            return
        if mise == None:
            await ctx.reply("Vous devez choisir une mise ! ")
            return
        try:
            case = int(case)
            if case < 1 or case > 36:
                await ctx.reply("Vous devez choisir une case valide !")
                return
        except:
            if case == "pair" or case == "impair" or case == "rouge" or case == "noir" or case == "vert":
                pass
            else:
                await ctx.reply("Vous devez choisir une case valide !")
                return
        try:
            mise = int(mise)
        except:
            await ctx.reply("Vous devez choisir une mise valide !")
            return
        if mise < 1:
            await ctx.reply("Vous devez choisir une mise supérieure à 0.")
            return
        if mise > 1000:
            await ctx.reply("Vous devez choisir une mise inférieure à 1,000.")
            return
        if int(u["coins"]) >= mise:
            if ctx.author.id in isrool:
                await ctx.reply("Vous avez déjà une partie en cours.")
                return
            isrool.append(ctx.author.id)
            embed=interactions.Embed(title="🎰 Roulette",description=f"La roulette est lancée, rien ne va plus !\n\n**Case choisie** : *{case}*\n")
            embed1=interactions.Embed(title="🎰 Roulette",description=f"La roulette est lancée, rien ne va plus !\n\n **Status:** :euro:")
            embed2=interactions.Embed(title="🎰 Roulette",description=f"La roulette est lancée, rien ne va plus !\n\n **Status:** :euro: :pound:")
            embed3=interactions.Embed(title="🎰 Roulette",description=f"La roulette est lancée, rien ne va plus !\n\n **Status:** :euro: :pound: :dollar:")
            
            embed.set_footer(text=self.bot.config["footer"])
            embed1.set_footer(text=self.bot.config["footer"])
            embed2.set_footer(text=self.bot.config["footer"])
            embed3.set_footer(text=self.bot.config["footer"])

            msg=await ctx.reply(embed=embed)
            self.bot.bdd.set_coins(u["coins"]-mise,ctx.author.id)
            await asyncio.sleep(1)
            await msg.edit(embed=embed1)
            await asyncio.sleep(1)
            await msg.edit(embed=embed2)
            await asyncio.sleep(1)
            await msg.edit(embed=embed3)
            result = random.randint(0,36)
            u=self.bot.bdd.check_user(ctx.author.id)[0]
            if result % 2 == 0:
                couleur = "🟥"
                pairImpair = "pair"
            else:
                couleur = "⬛"
                pairImpair = "impair"
            if result == 0:
                couleur = "🟩"
                pairImpair = "impair"

            if result == case:
                embed=interactions.Embed(title=f"🎰 Roulette",description=f"Case choisie : {case}\nCase tirée : {result} {pairImpair} {couleur}\n\n**Résultat**\nFélicitation ! Vous avez gagné {"{:,}".format(mise*12)}")
                embed.set_footer(text=self.bot.config["footer"])
                await ctx.reply(embed=embed)
                self.bot.bdd.set_coins(u["coins"]+mise*12,ctx.author.id)
                await generate_log_embed(self.bot,f"{ctx.author.mention} a gagné {"{:,}".format(mise*12)} coins à la roulette.")

            elif result % 2 == 0 and (case == "pair" or case == "rouge"):
                embed=interactions.Embed(title=f"🎰 Roulette",description=f"Case choisie : {case}\nCase tirée : {result} ,{pairImpair} ({couleur})\n\n**Résultat**\nFélicitation ! Vous avez gagné {"{:,}".format(mise*2)}")
                embed.set_footer(text=self.bot.config["footer"])
                await ctx.reply(embed=embed)
                self.bot.bdd.set_coins(u["coins"]+mise*2,ctx.author.id)
                await generate_log_embed(self.bot,f"{ctx.author.mention} a gagné {"{:,}".format(mise*2)} coins à la roulette.")

            elif result % 2 != 0 and (case == "impair" or case == "noir"):
                embed=interactions.Embed(title=f"🎰 Roulette",description=f"Case choisie : {case}\nCase tirée : {result}, {pairImpair} ({couleur})\n\n**Résultat**\nFélicitation ! Vous avez gagné {"{:,}".format(mise*2)}")
                embed.set_footer(text=self.bot.config["footer"])
                await ctx.reply(embed=embed)
                self.bot.bdd.set_coins(u["coins"]+mise*2,ctx.author.id)
                await generate_log_embed(self.bot,f"{ctx.author.mention} a gagné {"{:,}".format(mise*2)} coins à la roulette.")

            elif result == 0 and case == "vert":
                embed=interactions.Embed(title=f"🎰 Roulette",description=f"Case choisie : {case}\nCase tirée : {result}, {pairImpair} ({couleur})\n\n**Résultat**\nFélicitation ! Vous avez gagné {"{:,}".format(mise*12)}")
                embed.set_footer(text=self.bot.config["footer"])
                await ctx.reply(embed=embed)
                self.bot.bdd.set_coins(u["coins"]+mise*12,ctx.author.id)
                await generate_log_embed(self.bot,f"{ctx.author.mention} a gagné {"{:,}".format(mise*12)} coins à la roulette.")
            else:
                embed=interactions.Embed(title="🎰 Roulette",description=f"Case choisie : {case}\nCase tirée : {result}, {pairImpair} ({couleur})\n\n**Résultat**\nVous avez perdu, la prochaine sera la bonne... ou pas !")
                embed.set_footer(text=self.bot.config["footer"])
                await ctx.reply(embed=embed)
                await generate_log_embed(self.bot,f"{ctx.author.mention} a perdu {"{:,}".format(mise)} coins à la roulette.")
            isrool.remove(ctx.author.id)
        else:
            await ctx.reply("Vous n'avez pas assez de coins !")
        return