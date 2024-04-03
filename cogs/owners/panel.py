import discord
from discord.ui import Button
from discord import ButtonStyle
from discord.ext import commands
from utils import console

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def panel(self, ctx):
        if ctx.author.id in self.bot.config["owners"]:
            console.log(f"panel | {ctx.author} ({ctx.author.id})")
            embed = discord.Embed(title="Panel", description="Panel de gestion du bot", color=0x00ff00)
    #         view = discord.ui.View()
    #         buttons = [
    #     Button(style=ButtonStyle.primary, label="Profil", custom_id="profile"),
    #     Button(style=ButtonStyle.primary, label="Roulette", custom_id="rools"),
    #     Button(style=ButtonStyle.primary, label="Shop", custom_id="shop"),
    #     Button(style=ButtonStyle.primary, label="Inventaire", custom_id="inventory")
    # ]
    #         view.add_item(buttons)
            await ctx.send(embed=embed, view=view)
            
    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        if interaction.author.id in self.bot.config["owners"]:
            if interaction.custom_id == "profile":
                console.log(f"panel | {interaction.author} ({interaction.author.id}) | profile")
                await interaction.respond(content="Profile")
            elif interaction.custom_id == "rools":
                console.log(f"panel | {interaction.author} ({interaction.author.id}) | rools")
                await interaction.respond(content="Roulette")
            elif interaction.custom_id == "shop":
                console.log(f"panel | {interaction.author} ({interaction.author.id}) | shop")
                await interaction.respond(content="Shop")
            elif interaction.custom_id == "inventory":
                console.log(f"panel | {interaction.author} ({interaction.author.id}) | inventory")
                await interaction.respond(content="Inventaire")
            else:
                await interaction.respond(content="Erreur")
        else:
            await interaction.respond(content="Vous n'avez pas la permission d'utiliser ce panel")


async def setup(bot):
    await bot.add_cog(Panel(bot))