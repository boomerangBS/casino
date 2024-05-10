# COLIS COMMAND
# drop colis (embed avec bouton pour claim)
#permissions requises : wl
import interactions,asyncio,random
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from datetime import datetime
from utils import console,generate_log_embed
from datetime import datetime,timedelta

class Coliss(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def colis(self, ctx):
        check = self.bot.bdd.check_user(ctx.author.id)
        if check != []:
            check = check[0]
            if check["permissions"] == "wl" or ctx.author.id in self.bot.config["owners"]:
                console.log(f"colis | {ctx.author} ({ctx.author.id})")
                embed = interactions.Embed(title="📦 Drop",description="Clique sur le bouton en premier pour obtenir la récompense.")
                embed.set_footer(text="Vous devez être en vocal pour remporter la récompense")
                button = [Button(label="3",style=ButtonStyle.SUCCESS,custom_id="n",disabled=True),Button(label="2",style=ButtonStyle.SUCCESS,custom_id="n",disabled=True),Button(label="1",style=ButtonStyle.SUCCESS,custom_id="n",disabled=True)]
                m=await ctx.send(embed=embed)
                for i in range(3):
                    await asyncio.sleep(1)
                    await m.edit(components=[button[i]])
                await asyncio.sleep(1)
                button = Button(label="Obtenir !",style=ButtonStyle.SUCCESS,custom_id="claim")
                await m.edit(components=[button])
                try:
                    def check(i):
                        if i.ctx.message.id == m.id:
                            return True
                    i=await self.bot.wait_for_component(components=button,timeout=60,check=check)
                    button=Button(label="Obtenir !",style=ButtonStyle.SUCCESS,custom_id="t",disabled=True)
                    if i.ctx.custom_id == "claim":
                        cc=self.bot.bdd.check_user(i.ctx.author.id)
                        if cc == []:
                            embed = interactions.Embed(title="📦 Drop",description=f"{i.ctx.author.mention} a ouvert le colis mais il n'a pas créé son profil, il n'a rien gagné ❌.")
                            embed.set_footer(text="Vous devez être en vocal pour remporter la récompense")
                            await i.ctx.edit_origin(embed=embed,components=button)
                            return
                        bdd=self.bot.bdd
                        lastuse = bdd.get_countdown(i.ctx.author.id,"colis")
                        if isinstance(lastuse, datetime):
                            time_diff = datetime.now() - lastuse
                        else:
                            time_diff = datetime.now() - datetime.strptime(lastuse,"%Y-%m-%d %H:%M:%S")
                        if time_diff < timedelta(hours=12):
                            time_left = timedelta(hours=12) - time_diff
                            hours, remainder = divmod(time_left.seconds, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            cccccc = bdd.get_gamedata("colis",i.ctx.author.id)
                            if cccccc != []:
                                if int(cccccc[0]["datavalue"]) >= 5:
                                    embed = interactions.Embed(title="📦 Drop",description=f"{i.ctx.author.mention} a déjà ouvert 5 colis aujourd'hui, il n'a rien gagné :x:.")
                                    embed.set_footer(text="Vous devez être en vocal pour remporter la récompense")
                                    await i.ctx.edit_origin(embed=embed,components=button)
                                    return
                                else:
                                    bdd.set_gamedata("colis",i.ctx.author.id,int(cccccc[0]["datavalue"])+1)
                            else:
                                bdd.add_gamedata("colis",i.ctx.author.id,1)
                            # return
                        else:
                            cccccc = bdd.get_gamedata("colis","count")
                            if cccccc != []:
                                if cccccc[0]["datavalue"] >= 5:
                                    bdd.set_gamedata("colis",i.ctx.author.id,1)
                                else:
                                    bdd.set_gamedata("colis",i.ctx.author.id,cccccc[0]["datavalue"]+1)
                            else:
                                bdd.add_gamedata("colis",i.ctx.author.id,1)
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        bdd.set_countdown(i.ctx.author.id,"colis",now)
                        #check if author is in vc
                        uu=i.ctx.author
                        if uu is None:
                            embed = interactions.Embed(title="📦 Drop",description=f"{i.ctx.author.mention} a ouvert le colis mais il n'était pas en vocal, il n'a rien gagné :x:.")
                            embed.set_footer(text="Vous devez être en vocal pour remporter la récompense")
                            await i.ctx.edit_origin(embed=embed,components=button)
                            return
                        if uu.voice is not None and uu.voice.channel is not None:
                            if uu.voice.channel.guild.id != self.bot.config["guildid"]:
                                embed = interactions.Embed(title="📦 Drop",description=f"{i.ctx.author.mention} a ouvert le colis mais il n'était pas en vocal, il n'a rien gagné :x:.")
                                embed.set_footer(text="Vous devez être en vocal pour remporter la récompense")
                                await i.ctx.edit_origin(embed=embed,components=button)
                                return
                        else:
                            embed = interactions.Embed(title="📦 Drop",description=f"{i.ctx.author.mention} a ouvert le colis mais il n'était pas en vocal, il n'a rien gagné :x:.")
                            embed.set_footer(text="Vous devez être en vocal pour remporter la récompense")
                            await i.ctx.edit_origin(embed=embed,components=button)
                            return
                        coins=random.randint(1,5000)
                        points=random.randint(0,3)
                        tokens=random.randint(0,3)
                        pillages=random.randint(0,3)
                        self.bot.bdd.query(f"UPDATE profiles SET coins=coins+{coins},points=points+{points},tokens=tokens+{tokens},rob_availables=rob_availables+{pillages} WHERE id={ctx.author.id}.")
                        await generate_log_embed(self.bot,f"{i.ctx.author.mention} a ouvert le colis, il a remporté {"{:,}".format(int(coins))} coins, {points} point, {tokens} jetons et {pillages} pillages")
                        embed = interactions.Embed(title="📦 Drop",description=f"{i.ctx.author.mention} a ouvert un colis, il a gagné : \n- {"{:,}".format(int(coins))} coins\n- {points} point(s)\n- {tokens} jeton(s)\n- {pillages} pillage(s)")
                        embed.set_footer(text="Vous devez être en vocal pour remporter la récompense")
                        await i.ctx.edit_origin(embed=embed,components=button)
                except Exception as e:
                    button=Button(label="Obtenir !",style=ButtonStyle.SUCCESS,custom_id="t",disabled=True)
                    await m.edit(components=button)
