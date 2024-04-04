from interactions import Extension,component_callback
from utils import console
class PanelEventProfile(Extension):
    def __init__(self, bot):
        self.bot = bot

    @component_callback("profile")
    async def panel_profile_callback(self,ctx):
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            bdd.create_user(ctx.author.id)
            await ctx.send("Votre profil a bien été créé. On vous offre d'ailleurs 5 jetons pour commencer l'aventure. Tu peux tourner la roulette avec les jetons, que la chance soit avec toi ! ",ephemeral=True)
            console.action(f"Profile created for {ctx.author} ({ctx.author.id})")
        else:
            await ctx.send(content=str(u[0]))