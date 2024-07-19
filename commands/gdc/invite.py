import interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import generate_log_embed

class Invite(Extension):
    def __init__(self, bot):
        self.bot = bot
    
    @prefixed_command()
    async def invite(self, ctx, user=None):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
        bdd=self.bot.bdd
        status=bdd.get_gamedata("gdc","status")
        channel=bdd.get_gamedata("gdc","channel")
        if status == []:
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if status[0]["datavalue"] == "off":
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if channel == []:
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if channel[0]["datavalue"] == "NO":
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if ctx.channel.id != int(channel[0]["datavalue"]):
            await ctx.reply(f"Cette commande est uniquement utilisable dans <#{channel[0]["datavalue"]}>")
            return
        u=bdd.check_user(ctx.author.id)
        if u == []:
            return
        u=u[0]
        if user == None:
            await ctx.reply("Vous devez mentionner un utilisateur !")
            return
        if u["clan"] != None:
            if u["clan"] != "":
                check = bdd.check_clan(u["clan"])
                if check == []:
                    await ctx.reply("Votre clan n'existe pas (ceci es une erreur) !")
                    return
                check = check[0]
                if check["owner"] != ctx.author.id:
                    await ctx.reply("Vous n'êtes pas le chef de clan !")
                    return
                try:
                    user = int(user)
                except:
                    user = user.replace("<","").replace(">","").replace("@","").replace("!","")
                try:
                    user = self.bot.get_user(user)
                except:
                    user = None
                if user == None:
                    await ctx.reply("Utilisateur introuvable !")
                    return
                if user.id == ctx.author.id:
                    await ctx.reply("Vous ne pouvez pas vous inviter vous-même !")
                    return
                if user.bot:
                    await ctx.reply("Vous ne pouvez pas inviter un bot !")
                    return
                members=bdd.get_users_in_clan(u["clan"])
                if user.id in [i["id"] for i in members]:
                    await ctx.reply("Cet utilisateur est déjà dans votre clan !")
                    return
                gdcdata=bdd.get_gamedata('gdc','maxmembers')
                if len(check["members"]) >= gdcdata[0]["datavalue"]:
                    await ctx.reply("Votre clan est complet !")
                    return
                embed=interactions.Embed(title="Invitation",description=f"{ctx.author.mention} vous invite à rejoindre le clan **{check['name']}**")
                buttons = [interactions.Button(style=1, label="Accepter", custom_id="accept_invite"),interactions.Button(style=4, label="Refuser", custom_id="decline_invite")]
                mm=await ctx.send(f"{user.mention}")
                m=await ctx.send(embed=embed, components=buttons)
                try:
                    res=await self.bot.wait_for_component(components=buttons,timeout=600,check=lambda i: i.ctx.author.id == user.id and i.ctx.message.id == m.id)
                except:
                    await ctx.reply("Temps écoulé.")
                    await m.edit(components=[])
                    return
                res = res.ctx
                if res.custom_id == "decline_invite":
                    await res.send("Invitation refusée.")
                    await m.edit(components=[])
                    await mm.delete()
                    return
                elif res.custom_id == "accept_invite":
                    check = bdd.check_clan(u["clan"])[0]
                    gdcdata=bdd.get_gamedata('gdc','maxmembers')
                    if len(check["members"]) >= gdcdata[0]["datavalue"]:
                        await ctx.reply("Votre clan est complet !")
                        return
                    bdd.set_clan(u["clan"],user.id)
                    await res.send(f"{user.mention} a rejoint le clan avec succès !")
                    await m.edit(components=[])
                    await mm.delete()
                    await generate_log_embed(self.bot,f"{user.mention} a rejoint le clan {check['name']} ({check['id']}).")
                    return
            else:
                await ctx.reply("Vous n'êtes pas dans un clan !")
                return
        else:
            await ctx.reply("Vous n'êtes pas dans un clan !")
            return
                