import interactions
from interactions import Extension,component_callback
from utils import console

class PanelEventInventory(Extension):
    def __init__(self, bot):
        self.bot = bot

    @component_callback("inventory")
    async def panel_inventory_callback(self,ctx):
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        badges = bdd.get_badges(u["id"])
        if badges == None:
            await ctx.send(":information_source: Vous n'avez pas de badges !",ephemeral=True)
            return
        if u["badges"] == None:
                badges = []
        else:
            if "," in str(u["badges"]):
                badges = str(u["badges"]).split(",")
            else:
                badges = [str(u["badges"])]
        if len(badges) == 0:
            await ctx.send(":information_source: Vous n'avez pas de badges !",ephemeral=True)
            return
        
        
