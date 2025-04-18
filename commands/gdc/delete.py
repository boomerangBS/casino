import interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import generate_log_embed
class Delete(Extension):
    def __init__(self, bot):
        self.bot = bot
    
    @prefixed_command()
    async def delete(self, ctx):
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
        if u["clan"] != None:
            if u["clan"] != "":
                check = bdd.check_clan(u["clan"])
                if check == []:
                    await ctx.reply("Votre clan n'existe pas (ceci es une erreur) !")
                    return
                check = check[0]
                if check["owner"] == ctx.author.id:
                    embed = interactions.Embed(title="Supprimer le clan",description=f"Êtes-vous sûr de vouloir supprimer le clan {check['name']} ({check['id']}) ?",color=0x2F3136)
                    buttons = [interactions.Button(style=1, label="Oui", custom_id="del_clan_yes"),interactions.Button(style=4, label="Non", custom_id="del_clan_no")]
                    m=await ctx.reply(embed=embed, components=buttons)
                    try:
                        res=await self.bot.wait_for_component(components=buttons,timeout=60,check=lambda i: i.ctx.author.id == ctx.author.id and i.ctx.message.id == m.id)
                    except:
                        await ctx.reply("Temps écoulé.")
                        return
                    res = res.ctx
                    if res.custom_id == "del_clan_no":
                        await res.send("Action annulée.")
                        await m.edit(components=[])
                        return
                    elif res.custom_id == "del_clan_yes":
                        await m.edit(components=[])
                        bdd.delete_clan(u["clan"])
                        users = bdd.get_users_in_clan(u["clan"])
                        for user in users:
                            bdd.set_clan("",user["id"])
                        await ctx.reply("Votre clan a été supprimé avec succès !")
                        await generate_log_embed(self.bot,f"Le clan {check['name']} ({check['id']}) a été supprimé par {ctx.author.mention}.")
                        return
                else:
                    await ctx.reply("Vous n'êtes pas le chef de clan !")
                    return
            else:
                await ctx.reply("Vous n'êtes pas dans un clan !")
                return
        else:
            await ctx.reply("Vous n'êtes pas dans un clan !")
            return