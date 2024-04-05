import interactions
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
class Panel(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def panel(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            console.log(f"panel | {ctx.author} ({ctx.author.id})")
            ctoken = self.bot.bdd.get_tokens_settings()[0]
            embed = interactions.Embed(title=f"Casino {ctx.guild.name}",description=f"""👤 `Profil : `
> Création de votre profil puis vous permet de le consulter (Nombre de jetons, nombre de points, nombre de coins) 

🍀 `Roulette :` 
> Vous pouvez tourner la roue en ayant des jetons. Vous pouvez y gagner des rôles, des nitros, des coins. 

💎 `Shop :` 
> Vous permet d'acheter des rôles, des nitros ou autres avec vos Coins.

🗂️ `Inventaire :` 
> Vous permet de consulter votre inventaire et modifier vos rôles équipés.

🎟️ **Gain de jetons : **

- {ctoken['voice_hours']}h de voc = 1 jeton
- {ctoken['messages']} messages = 1 jeton
- {ctoken['status']} en statut = {ctoken['status_count']} jeton(s) toutes les {ctoken['status_time']}h""")
            embed.set_footer(text=self.bot.config["footer"])
            buttons = [
                Button(style=ButtonStyle.BLUE, label="Profil", custom_id="profile"),
                Button(style=ButtonStyle.BLUE, label="Roulette", custom_id="roulette"),
                Button(style=ButtonStyle.BLUE, label="Shop", custom_id="shop"),
                Button(style=ButtonStyle.BLUE, label="Inventaire", custom_id="inventory")
            ]
            await ctx.send(embed=embed, components=[buttons])
    
