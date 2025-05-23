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
            blcheck = bdd.check_blacklist(ctx.author.id)
            if blcheck != []:
                await ctx.send(":warning: Vous êtes sur la liste noire, vous ne pouvez pas créer de profil.",ephemeral=True)
                return
            bdd.create_user(ctx.author.id)
            await ctx.send("Votre profil a bien été créé. On vous offre d'ailleurs 5 jetons pour commencer l'aventure. Tu peux tourner la roulette avec les jetons, que la chance soit avec toi ! ",ephemeral=True)
            console.action(f"Profile created for {ctx.author} ({ctx.author.id})")
        else:
            u = u[0]
            if u['clan'] == None:
                u['clan'] = "Aucun clan"
            else:
                clan = bdd.check_clan(u['clan'])
                if clan != []:
                    clan = clan[0]
                    u['clan'] = clan["name"]
                else:
                    u['clan'] = "Clan inconnu"
            s=bdd.get_tokens_settings()[0]
            messages = s["messages"]-u["messages"]
            voice = s["voice_hours"]*60-u["voice_minutes"]
            embed = interactions.Embed(description=f"**__Profil de {ctx.author.display_name}__**\n\n:trophy: `Point(s)` ➟ **{u['points']}**\n:tickets: `Jeton(s)` ➟ **{u['tokens']}**\n:crossed_swords: `Pillage(s) disponible(s)` ➟ **{u['rob_availables']}**\n:coin: `Nombre de coins` ➟ **{"{:,}".format(u['coins'])}**\n:beginner: `Clan` ➟ **{u['clan']}**\n:incoming_envelope: `Messages restants`➟ **{messages} messages**\n:loud_sound: `Minutes de vocal restantes` ➟ **{voice} minutes**")
            embed.set_footer(text=self.bot.config['footer'])
            if ctx.author.avatar.url is not None:
                embed.set_thumbnail(url=ctx.author.avatar.url)
            else:
                embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
            await ctx.send(embed=embed,ephemeral=True)