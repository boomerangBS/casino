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
        # if badges == None:
        #     await ctx.send(":information_source: Vous n'avez pas de badges !",ephemeral=True)
        #     return
        if u["badges"] == None or u["badges"] == "":
                badges = []
        else:
            if "," in str(u["badges"]):
                badges = str(u["badges"]).split(",")
            else:
                badges = [str(u["badges"])]
        # if len(badges) == 0:
        #     await ctx.send(":information_source: Vous n'avez pas de badges !",ephemeral=True)
        #     return
        msg = ""
        equiped = []
        opt=[]
        for badge in badges:
            r = ctx.guild.get_role(int(badge))
            if r == None:
                continue
            msg += f"- <@&{badge}> \n"
            if r in ctx.author.roles:
                equiped.append(badge)
            else:
                opt.append(StringSelectOption(label=r.name,value=badge))
            
        if len(equiped) > 0:
            opt.append(StringSelectOption(label="Déséquiper vos badges",value="remove"))
            msg += "\n**Equipés** \n\n"
            for badge in equiped:
                r = ctx.guild.get_role(int(badge))
                if r == None:
                    continue
                msg += f"- <@&{badge}> \n"
        if msg == "":
            msg += "*Vous n'avez aucun badge dans votre inventaire*"
        embed = interactions.Embed(title="Inventaire",description=msg)
        embed.set_footer(text=self.bot.config["footer"])
        choice=interactions.Button(style=interactions.ButtonStyle.BLUE,label="Modifier vos badges",custom_id="edit_badges",disabled=True)
        if opt == []:
            await ctx.send(embed=embed,ephemeral=True,components=[choice])
            return
        choice = interactions.Button(style=interactions.ButtonStyle.BLUE,label="Modifier vos badges",custom_id="edit_badges")
        selectmenu = StringSelectMenu(opt,custom_id="equip_badge",placeholder="Selectionnez un badge à équiper",min_values=1,max_values=1)
        c=await ctx.send(embed=embed,ephemeral=True,components=[choice])
        try:
            i=await self.bot.wait_for_component(components=choice,timeout=200,check=lambda i: i.ctx.author.id == ctx.author.id and i.ctx.message.id == c.id)
            if i.ctx.custom_id == "edit_badges":
                await i.ctx.send("Choisisez un badge a équiper",ephemeral=True,components=[selectmenu])
                choice.disabled = True
                await i.ctx.message.edit_origin(components=[choice])
        except:
            await c.edit(components=[])
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
        
        
        
