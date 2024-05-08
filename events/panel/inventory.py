import interactions
from interactions import Extension,component_callback,StringSelectMenu,StringSelectOption
from utils import console

class PanelEventInventory(Extension):
    def __init__(self, bot):
        self.bot = bot

    @component_callback("inventory")
    async def panel_inventory_callback(self,ctx):
        console.log(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id})")
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        badges = bdd.get_badges(u["id"])
        if u["badges"] == None or u["badges"] == "":
                badges = []
        else:
            if "," in str(u["badges"]):
                badges = str(u["badges"]).split(",")
            else:
                badges = [str(u["badges"])]
        colors = bdd.get_colors(u["id"])
        if u["colors"] == None or u["colors"] == "":
            colors = []
        else:
            if "," in str(u["colors"]):
                colors = str(u["colors"]).split(",")
            else:
                colors = [str(u["colors"])]
        badgemsg = ""
        colormsg = ""
        badgesopt=[]
        colorsopt=[]
        badgesequiped=[]
        colorsequiped=[]
        for badge in badges:
            r = ctx.guild.get_role(int(badge))
            if r == None:
                continue
            badgemsg += f"<@&{badge}> \n"
            if r in ctx.author.roles:
                badgesequiped.append(badge)
            else:
                badgesopt.append(StringSelectOption(label=r.name,value=badge))
        if badgemsg == "":
                badgemsg += "Aucun badge"
        for color in colors:
            r = ctx.guild.get_role(int(color))
            if r == None:
                continue
            colormsg += f"<@&{color}> \n"
            if r in ctx.author.roles:
                colorsequiped.append(color)
            else:
                colorsopt.append(StringSelectOption(label=r.name,value=color))
        if colormsg == "":
            colormsg += "Aucune couleur"
        embed = interactions.Embed(title="Inventaire")
        embed.set_footer(text=self.bot.config["footer"])
        embed.add_field(name="Badges",value=badgemsg,inline=True)
        embed.add_field(name="Couleurs",value=colormsg,inline=True)
        choice=[interactions.Button(style=interactions.ButtonStyle.BLUE,label="Modifier vos badges",custom_id="edit_badges"),interactions.Button(style=interactions.ButtonStyle.BLUE,label="Modifier vos couleurs",custom_id="edit_colors")]
        dchoice=[interactions.Button(style=interactions.ButtonStyle.BLUE,label="Modifier vos badges",custom_id="edit_badges",disabled=True),interactions.Button(style=interactions.ButtonStyle.BLUE,label="Modifier vos couleurs",custom_id="edit_colors",disabled=True)]
        if badgesequiped != []:
            badgesopt.append(StringSelectOption(label="Déséquiper votre badge",value="remove"))
        if colorsequiped != []:
            colorsopt.append(StringSelectOption(label="Déséquiper votre couleur",value="remove"))
        badgesmenu = StringSelectMenu(badgesopt,custom_id="equip_badge",placeholder="Selectionnez un badge à équiper",min_values=1,max_values=1)
        colorsmenu = StringSelectMenu(colorsopt,custom_id="equip_color",placeholder="Selectionnez une couleur à équiper",min_values=1,max_values=1)
        c=await ctx.send(embed=embed,ephemeral=True,components=[choice])
        try:
            i=await self.bot.wait_for_component(components=choice,timeout=200,check=lambda i: i.ctx.author.id == ctx.author.id and i.ctx.message.id == c.id)
            if i.ctx.custom_id == "edit_badges":
                await i.ctx.edit_origin(components=[dchoice])
                if badgesopt == [] and badgesequiped == []:
                    await ctx.send(content="Vous n'avez pas de badge à équiper !",ephemeral=True)
                    return
                await ctx.send("Choisisez un badge a équiper",ephemeral=True,components=[badgesmenu])
            if i.ctx.custom_id == "edit_colors":
                await i.ctx.edit_origin(components=[dchoice])
                if colorsopt == [] and colorsequiped == []:
                    await ctx.send("Vous n'avez pas de couleur à équiper !",ephemeral=True)
                    return
                await ctx.send("Choisisez une couleur a équiper",ephemeral=True,components=[colorsmenu])
        except:
            return
    
    

    @component_callback("equip_badge")
    async def equip_badge(self,ctx):
        console.log(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id})")
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        if ctx.values[0] == "remove":
            badges = bdd.get_badges(u["id"])
            if badges == None:
                await ctx.send(":information_source: Vous n'avez pas d'item !",ephemeral=True)
                return
            if u["badges"] == None or u["badges"] == "":
                badges = []
            else:
                if "," in str(u["badges"]):
                    badges = str(u["badges"]).split(",")
                else:
                    badges = [str(u["badges"])]
            if len(badges) == 0:
                await ctx.send(":information_source: Vous n'avez pas de badge !",ephemeral=True)
                return
            for badge in badges:
                r = ctx.guild.get_role(int(badge))
                if r == None:
                    continue
                if r in ctx.author.roles:
                    try:
                        await ctx.author.remove_role(r)
                    except:
                        await ctx.send(f":information_source: Une erreur est survenue lors du déséquipement du badge {r.name} !",ephemeral=True)
                        console.warning(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id}) failed to unequip badge {r.name}")
            await ctx.send(":white_check_mark: Vous avez déséquipé tous vos badges !",ephemeral=True)
            return
        badges = bdd.get_badges(u["id"])
        if badges == None:
            await ctx.send(":information_source: Vous n'avez pas d'item !",ephemeral=True)
            return
        if u["badges"] == None or u["badges"] == "":
                badges = []
        else:
            if "," in str(u["badges"]):
                badges = str(u["badges"]).split(",")
            else:
                badges = [str(u["badges"])]
        if len(badges) == 0:
            await ctx.send(":information_source: Vous n'avez pas de badge !",ephemeral=True)
            return
        badge = None
        for i in badges:
            if i == ctx.values[0]:
                badge = i
                break
        if badge == None:
            await ctx.send(":information_source: Ce badge n'existe pas dans votre inventaire !",ephemeral=True)
            return
        r = ctx.guild.get_role(int(badge))
        if r == None:
            await ctx.send(":information_source: Ce badge n'existe pas dans votre inventaire !",ephemeral=True)
            return
        if r in ctx.author.roles:
            await ctx.send(":information_source: Ce badge est déjà équipé !",ephemeral=True)
            return
        for b in badges:
            if b == badge:
                continue
            r2 = ctx.guild.get_role(int(b))
            if r2 == None:
                continue
            if r2 in ctx.author.roles:
                try:
                    await ctx.author.remove_role(r2)
                except:
                    await ctx.send(":information_source: Une erreur est survenue lors de l'équipement du badge ! (2)",ephemeral=True)
                    console.warning(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id}) failed to unequip badge {r2.name}")
                    return
        try:
            await ctx.author.add_role(r)
        except:
            await ctx.send(":information_source: Une erreur est survenue lors de l'équipement du badge !",ephemeral=True)
            console.warning(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id}) failed to equip badge {r.name}")
            return
        await ctx.send(f":white_check_mark: Vous avez équipé le badge {r.mention} !",ephemeral=True)
        return
        
    @component_callback("equip_color")
    async def equip_color(self,ctx):
        console.log(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id})")
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        if ctx.values[0] == "remove":
            colors = bdd.get_colors(u["id"])
            if colors == None:
                await ctx.send(":information_source: Vous n'avez pas d'item !",ephemeral=True)
                return
            if u["colors"] == None or u["colors"] == "":
                colors = []
            else:
                if "," in str(u["colors"]):
                    colors = str(u["colors"]).split(",")
                else:
                    colors = [str(u["colors"])]
            if len(colors) == 0:
                await ctx.send(":information_source: Vous n'avez pas de couleur !",ephemeral=True)
                return
            for color in colors:
                r = ctx.guild.get_role(int(color))
                if r == None:
                    continue
                if r in ctx.author.roles:
                    try:
                        await ctx.author.remove_role(r)
                    except:
                        await ctx.send(f":information_source: Une erreur est survenue lors du déséquipement de la couleur {r.name} !",ephemeral=True)
                        console.warning(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id}) failed to unequip color {r.name}")
            await ctx.send(":white_check_mark: Vous avez déséquipé toutes vos couleurs !",ephemeral=True)
            return
        colors = bdd.get_colors(u["id"])
        if colors == None:
            await ctx.send(":information_source: Vous n'avez pas d'item !",ephemeral=True)
            return
        if u["colors"] == None or u["colors"] == "":
                colors = []
        else:
            if "," in str(u["colors"]):
                colors = str(u["colors"]).split(",")
            else:
                colors = [str(u["colors"])]
        if len(colors) == 0:
            await ctx.send(":information_source: Vous n'avez pas de couleur !",ephemeral=True)
            return
        color = None
        for i in colors:
            if i == ctx.values[0]:
                color = i
                break
        if color == None:
            await ctx.send(":information_source: Cette couleur n'existe pas dans votre inventaire !",ephemeral=True)
            return
        r = ctx.guild.get_role(int(color))
        if r == None:
            await ctx.send(":information_source: Cette couleur n'existe pas dans votre inventaire !",ephemeral=True)
            return
        
        if r in ctx.author.roles:
            await ctx.send(":information_source: Cette couleur est déjà équipée !",ephemeral=True)
            return
        for c in colors:
            if c == color:
                continue
            r2 = ctx.guild.get_role(int(c))
            if r2 == None:
                continue
            if r2 in ctx.author.roles:
                try:
                    await ctx.author.remove_role(r2)
                except:
                    await ctx.send(":information_source: Une erreur est survenue lors de l'équipement de la couleur ! (2)",ephemeral=True)
                    console.warning(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id}) failed to unequip color {r2.name}")
                    return
        try:
            await ctx.author.add_role(r)
        except:
            await ctx.send(":information_source: Une erreur est survenue lors de l'équipement de la couleur !",ephemeral=True)
            console.warning(f"[INVENTORY] panel_inventory_callback | {ctx.author} ({ctx.author.id}) failed to equip color {r.name}")
            return
        await ctx.send(f":white_check_mark: Vous avez équipé la couleur {r.mention} !",ephemeral=True)
        return
        
        
