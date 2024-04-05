import interactions
from interactions import Extension,component_callback
from utils import console
class PanelEventProfile(Extension):
    def __init__(self, bot):
        self.bot = bot

    @component_callback("profile")
    async def panel_profile_callback(self,ctx):
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            bdd.create_user(ctx.author.id)
            await ctx.send("Votre profil a bien été créé. On vous offre d'ailleurs 5 jetons pour commencer l'aventure. Tu peux tourner la roulette avec les jetons, que la chance soit avec toi ! ",ephemeral=True)
            console.action(f"Profile created for {ctx.author} ({ctx.author.id})")
        else:
            u = u[0]
            if u['clan'] == None:
                u['clan'] = "Aucun clan"
            embed = interactions.Embed(description=f"**__Profil de l'utilisateur__**\n\n:trophy: `Point(s)` ➟ **{u['points']}**\n:tickets: `Jeton(s)` ➟ **{u['tokens']}**\n:crossed_swords: `Pillage(s) disponible(s)` ➟ **{u['rob_availables']}**\n:coin: `Nombre de coins` ➟ **{u['coins']}**\n:beginner: `Clan` ➟ **{u['clan']}**")
            embed.set_footer(text=self.bot.config['footer'])
            if ctx.author.avatar.url is not None:
                embed.set_thumbnail(url=ctx.author.avatar.url)
            else:
                embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            await ctx.send(embed=embed,ephemeral=True)