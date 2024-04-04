from interactions import Extension,component_callback
from utils import console
class PanelEventRoulette(Extension):
    def __init__(self, bot):
        self.bot = bot

    @component_callback("roulette")
    async def panel_roulette_callback(self,ctx):
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            pass