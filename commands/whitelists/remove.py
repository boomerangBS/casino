# REMOVE COMMAND
#remove <type:coins,jetons,pillages,points> <user> <amount> : enleve des points, jetons, pillages ou coins à un utilisateur.
# permissions requises : wl,owner
import interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class Remove(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def remove(self, ctx,type=None,user=None,amount:int=None):
        bdd=self.bot.bdd
        u = bdd.check_user(ctx.author.id)
        if u != []:
            u = u[0]
            if u["permissions"] == "wl" or ctx.author.id in self.bot.config["owners"]:
                if type in ["coins","jetons","pillages","points"]:
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
                            user = user[0]
                        else:
                            await ctx.send("Cet utilisateur n'existe pas (ou n'est pas inscrit) !")
                            return
                        if amount is not None:
                            try:
                                amount = int(amount)
                            except:
                                await ctx.send("Montant invalide !")
                                return
                            if type == "coins":
                                bdd.set_coins(user["coins"] - amount, uid)
                                await ctx.send(f"{amount} Coins enlevés à <@{uid}>")
                                console.log(f"remove | {ctx.author} ({ctx.author.id}) | {amount} coins enlevés à {uid}")
                            if type == "jetons":
                                bdd.set_tokens(user["tokens"] - amount, uid)
                                await ctx.send(f"{amount} Jetons enlevés à <@{uid}>")
                                console.log(f"remove | {ctx.author} ({ctx.author.id}) | {amount} jetons enlevés à {uid}")
                            if type == "pillages":
                                bdd.set_pillages(user["rob_availables"] - amount, uid)
                                await ctx.send(f"{amount} Pillages enlevés à <@{uid}>")
                                console.log(f"remove | {ctx.author} ({ctx.author.id}) | {amount} pillages enlevés à {uid}")
                            if type == "points":
                                bdd.set_points(user["points"] - amount, uid)
                                await ctx.send(f"{amount} Points enlevés à <@{uid}>")
                                console.log(f"remove | {ctx.author} ({ctx.author.id}) | {amount} points enlevés à {uid}")
                        else:
                            await ctx.send("Arguments invalide, ``remove <type:coins,jetons,pillages,points> <user> <amount>``")
                    else:
                        await ctx.send("Arguments invalide, remove ``<type:coins,jetons,pillages,points> <user> <amount>``")
                else:
                    await ctx.send("Arguments invalide, remove ``<type:coins,jetons,pillages,points> <user> <amount>``")