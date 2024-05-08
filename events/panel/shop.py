import interactions
from interactions import Extension,component_callback,StringSelectMenu,StringSelectOption
from utils import console,generate_log_embed
import ast

class PanelEventShop(Extension):
    def __init__(self, bot):
        self.bot = bot
    
    @component_callback("shop")
    async def shop(self, ctx):
        console.log(f"[SHOP] panel_callback_shop | {ctx.author} ({ctx.author.id})")
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        shop = bdd.get_shop()
        if shop == []:
            await ctx.send(":information_source: Le magasion est vide pour le moment, revenez plus tard !",ephemeral=True)
            return
        desc = ""
        i=0
        menu = []
        for item in shop:
            i+=1
            if item["type"] == "role" or item["type"] == "badge" or item["type"] == "color":
                desc += f"{i}. **{item['name']}** ➟ **{"{:,}".format(item['price'])}** :coin:\n"
                menu.append(StringSelectOption(label=item["name"],value=item['id']))
            elif item["type"] == "coins":
                desc += f"{i}. **{item['name']}** ({item['data']} coins) ➟ **{"{:,}".format(item['price'])}** :coin:\n"
                menu.append(StringSelectOption(label=item["name"],value=item['id']))
            elif item["type"] == "jetons":
                desc += f"{i}. **{item['name']}** ({item['data']} jetons) ➟ **{"{:,}".format(item['price'])}** :coin:\n"
                menu.append(StringSelectOption(label=item["name"],value=item['id']))
            elif item["type"] == "pillages":
                desc += f"{i}. **{item['name']}** ({item['data']} pillages) ➟ **{"{:,}".format(item['price'])}** :coin:\n"
                menu.append(StringSelectOption(label=item["name"],value=item['id']))
        embed=interactions.Embed(title="Boutique",description=desc)
        embed.set_footer(text=self.bot.config["footer"])
        await ctx.send(embed=embed,components=[StringSelectMenu(menu,custom_id="shop_select",placeholder="Selectionnez un item à acheter",min_values=1,max_values=1)],ephemeral=True)

    @component_callback("shop_select")
    async def shop_select(self, ctx):
        console.log(f"[SHOP] panel_callback_shop_select | {ctx.author} ({ctx.author.id})")
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        shop = bdd.get_shop()
        if shop == []:
            await ctx.send(":information_source: Le magasion est vide pour le moment, revenez plus tard !",ephemeral=True)
            return
        item = None
        for i in shop:
            if i["id"] == int(ctx.values[0]):
                item = i
                break
        if item is None:
            await ctx.send(":information_source: Cet item n'existe pas (ou plus !) .",ephemeral=True)
            return
        if u["coins"] < item["price"]:
            await ctx.send(":information_source: Vous n'avez pas assez de coins pour acheter cet item !",ephemeral=True)
            return
       
        if item["type"] == "role":
            role = ctx.guild.get_role(item["data"])
            if role is None:
                await ctx.send(":information_source: Le role n'existe pas (ou plus !), veuillez contacter un administrateur.",ephemeral=True)
                return
            if role in ctx.author.roles:
                await ctx.send(":information_source: Vous possédez déjà ce role !",ephemeral=True)
                return
            try:
                await ctx.author.add_role(role)
            except Exception:
                await ctx.send(":x: Une erreur est survenue lors de l'ajout du role !",ephemeral=True)
                return
            bdd.set_coins(u["coins"] - item["price"],ctx.author.id)
            console.log(f"[SHOP] {ctx.author} ({ctx.author.id}) a acheté le role {role.name} pour {item['price']} coins")
            await ctx.send(f":white_check_mark: Vous avez acheté le role **{role.name}** pour **{item['price']}** :coin: !",ephemeral=True)
            await generate_log_embed(self.bot,f'<@{ctx.author.id}>  vient d\'acheter "{item["name"]}" pour {item["price"]} coins !')
        elif item["type"] == "badge":
            badge = str(item["data"])
            if u["badges"] == None:
                badges = []
            else:
                if "," in str(u["badges"]):
                    badges = str(u["badges"]).split(",")
                else:
                    badges = [str(u["badges"])]
            if badge in badges:
                await ctx.send(":information_source: Vous avez déjà ce badge !",ephemeral=True)
                return
            badges.append(badge)
            if len(badges) > 1:
                badges = ",".join(badges)
            else:
                badges = badges[0]
            bdd.set_coins(u["coins"] - item["price"],ctx.author.id)
            bdd.set_badges(badges,ctx.author.id)
            console.log(f"[SHOP] {ctx.author} ({ctx.author.id}) a acheté le badge {badge} pour {item['price']} coins !")
            await ctx.send(f":white_check_mark: Vous avez acheté le badge **{item['name']}** pour **{item['price']}** :coin: !",ephemeral=True)
            await generate_log_embed(self.bot,f'<@{ctx.author.id}>  vient d\'acheter "{item["name"]}" pour {item["price"]} coins !')
        elif item["type"] == "color":
            color = str(item["data"])
            if u["colors"] == None:
                colors = []
            else:
                if "," in str(u["colors"]):
                    colors = str(u["colors"]).split(",")
                else:
                    colors = [str(u["colors"])]
            if color in colors:
                await ctx.send(":information_source: Vous avez déjà cette couleur !",ephemeral=True)
                return
            colors.append(color)
            if len(colors) > 1:
                colors = ",".join(colors)
            else:
                colors = colors[0]
            bdd.set_coins(u["coins"] - item["price"],ctx.author.id)
            bdd.set_colors(colors,ctx.author.id)
            console.log(f"[SHOP] {ctx.author} ({ctx.author.id}) a acheté la couleur {color} pour {item['price']} coins !")
            await ctx.send(f":white_check_mark: Vous avez acheté la couleur **{item['name']}** pour **{item['price']}** :coin: !",ephemeral=True)
            await generate_log_embed(self.bot,f'<@{ctx.author.id}>  vient d\'acheter "{item["name"]}" pour {item["price"]} coins !')
        #Jsp pk j'ai fait ca mdr ca sert a rien d'acheter des coins mdr
        elif item["type"] == "coins":
            bdd.set_coins(u["coins"] - item["price"] + item["data"],ctx.author.id)
            console.log(f"[SHOP] {ctx.author} ({ctx.author.id}) a acheté {item['data']} coins pour {item['price']} coins !")
            await ctx.send(f":white_check_mark: Vous avez acheté **{item['data']}** coins pour **{item['price']}** :coin: !",ephemeral=True)
            await generate_log_embed(self.bot,f'<@{ctx.author.id}>  vient d\'acheter "{item["name"]}" pour {item["price"]} coins !')
        elif item["type"] == "jetons":
            bdd.set_coins(u["coins"] - item["price"],ctx.author.id)
            bdd.set_tokens(u["tokens"] + item["data"],ctx.author.id)
            console.log(f"[SHOP] {ctx.author} ({ctx.author.id}) a acheté {item['data']} jetons pour {item['price']} coins !")
            await ctx.send(f":white_check_mark: Vous avez acheté **{item['data']}** jetons pour **{item['price']}** :coin: !",ephemeral=True)
            await generate_log_embed(self.bot,f'<@{ctx.author.id}>  vient d\'acheter "{item["name"]}" pour {item["price"]} coins !')
        elif item["type"] == "pillages":
            bdd.set_coins(u["coins"] - item["price"],ctx.author.id)
            bdd.set_pillages(u["rob_availables"] + item["data"],ctx.author.id)
            console.log(f"[SHOP] {ctx.author} ({ctx.author.id}) a acheté {item['data']} pillages pour {item['price']} coins !")
            await ctx.send(f":white_check_mark: Vous avez acheté **{item['data']}** pillages pour **{item['price']}** :coin: !",ephemeral=True)
            await generate_log_embed(self.bot,f'<@{ctx.author.id}>  vient d\'acheter "{item["name"]}" pour {item["price"]} coins !')
        else:
            await ctx.send(":information_source: Cet item n'existe pas (ou plus !) (2)",ephemeral=True)