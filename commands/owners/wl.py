# WL COMMAND
#wl : show the whitelist
#wl <user> : add or remove user to the whitelist

import interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class Whitelist(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command(aliases=["wl"])
    async def whitelist(self,ctx,user=None):
        bdd=self.bot.bdd
        if ctx.author.id in self.bot.config["owners"]:
            if user is None:
                u = bdd.list_users()
                if u != []:
                    u = [f"<@{i['id']}> ({i['id']})" for i in u if i["permissions"] == "wl"]
                    if u == []:
                        desc="**Whitelist** \n\nAucun utilisateur dans la whitelist."
                    else:
                        desc="**Whitelist** \n"+"\n- ".join(u)
                else:
                    desc="**Whitelist** \n\nAucun utilisateur dans la whitelist."
                embed = interactions.Embed(description=desc)
                embed.set_footer(text="Utilisez &wl <user> pour ajouter ou retirer un utilisateur de la Whitelist.")
                await ctx.send(embed=embed)
            else:
                try:
                    user = int(user)
                except:
                    try:
                        user = int(user.split("<@")[1].split(">")[0])
                    except:
                        await ctx.send("Utilisateur invalide !")
                        return
                check=bdd.check_user(user)
                if check != []:
                    if check[0]["permissions"] == "wl":
                        bdd.set_permissions(user,"")
                        await ctx.send(f"<@{user}> ({user}) à bien été retiré de la whitelist.")
                    else:
                        bdd.set_permissions(user,"wl")
                        await ctx.send(f"<@{user}> ({user}) à bien été ajouté à la whitelist.")
                else:
                    await ctx.send("Cet utilisateur n'as pas de compte !")

