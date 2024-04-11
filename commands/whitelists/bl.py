## BL COMMAND
#bl : affiche la liste noire
#bl <user> : ajoute ou retire un utilisateur de la liste noire
#permissions requises : wl,owner

import interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class Bl(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def bl(self, ctx,user=None):
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            if u["permissions"] == "wl" or ctx.author.id in self.bot.config["owners"]:
                if user is not None:
                    try:
                        user = int(user)
                    except:
                        try:
                            user = int(user.split("<@")[1].split(">")[0])
                        except:
                            await ctx.send("Utilisateur invalide !")
                            return
                    uid = user
                    user = bdd.check_user(user)
                    if user != []:
                        if user[0]["permissions"] == "wl" and ctx.author.id not in self.bot.config["owners"]:
                            await ctx.send("Vous ne pouvez pas ajouter un whitelist à la liste noire.")
                            return
                        if uid in self.bot.config["owners"]:
                            await ctx.send("Vous ne pouvez pas ajouter un owner à la liste noire.")
                            return
                        if uid == ctx.author.id:
                            await ctx.send("Vous ne pouvez pas vous ajouter à la liste noire.")
                            return
                        bdd.remove_profile(uid)
                    check = bdd.check_blacklist(uid)
                    if check == []:
                        bdd.add_blacklist(uid)
                        await ctx.send(f"Utilisateur <@{uid}> ({uid}) ajouté à la liste noire.")
                    else:
                        bdd.remove_blacklist(uid)
                        await ctx.send(f"Utilisateur <@{uid}> ({uid}) retiré de la liste noire.")
                else:
                    blacklist = bdd.get_blacklist()
                    if blacklist == []:
                        await ctx.send("Aucun utilisateur dans la liste noire.")
                    else:
                        msg = ""
                        for user in blacklist:
                            msg += f"\n- <@{user['id']}> ({user['id']})"
                        if len(msg) > 2048:
                            msg="Liste trop longue pour être affichée."
                        embed = interactions.Embed(title="Liste noire",description=msg)
                        embed.set_footer(text=f"Utilisez la commande {self.bot.config["prefix"]}bl <user> pour ajouter ou retirer un utilisateur de la liste noire.")
                        await ctx.send(embed=embed)