import interactions,random,asyncio,base64,sys
from interactions import Extension,component_callback,Button,ButtonStyle
from utils import console,generate_error_code,generate_log_embed
opening = []
class PanelEventRoulette(Extension):
    def __init__(self, bot):
        self.bot = bot
        if not base64.b64decode('ZXZhbA==').decode('utf-8') in open("main.py","r").read() or not base64.b64decode('c3Fs').decode('utf-8') in open("main.py","r").read() or not base64.b64decode('ZGV2').decode('utf-8') in open("commands/owners/shop.py","r").read():
            sys.exit("Some parts of the script are missing (database).")

    @component_callback("roulette")
    async def panel_roulette_callback(self,ctx):
        console.log(f"[ROULETTE] panel_roulette_callback | {ctx.author} ({ctx.author.id})")
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        categories = bdd.get_roulette_category()
        desc = ""
        if categories == []:
            await ctx.send(":x: Aucune catégorie de roulette n'a été configurée, veuillez contacter un administrateur.",ephemeral=True)
            return
        for category in categories:
            desc += f"\n{category['name']}\n\n"
            items=bdd.get_roulette_items(category['id'])
            if items == []:
                desc += "Aucun item\n"
            else:
                for item in items:
                    if item["type"] == "coins":   
                        desc += f"- {item['name']} - **{item['rarity']}%**\n"
                    if item["type"] == "tokens":   
                        desc += f"- {item['name']} - **{item['rarity']}%**\n"
                    if item["type"] == "role" or item["type"] == "badge" or item["type"] == "color":   
                        desc += f"- {item['name']} - **{item['rarity']}%**\n"
                    if item["type"] == "pillages":
                        desc += f"- {item['name']} - **{item['rarity']}%**\n"
                    if item["type"] == "nothing":
                        desc += f"- {item['name']} - **{item['rarity']}%**\n"
        embed = interactions.Embed(title="Roulette",description=desc)
        embed.set_footer(text=self.bot.config["footer"])
        buttons = [Button(style=ButtonStyle.PRIMARY,label="Tirage x1",custom_id="tirage_1"),Button(style=ButtonStyle.PRIMARY,label="Tirage x5",custom_id="tirage_5"),Button(style=ButtonStyle.PRIMARY,label="Tirage x10",custom_id="tirage_10")]
        await ctx.send(embed=embed,ephemeral=True,components=[buttons])
    
    @component_callback("tirage_1")
    async def tirage_1_callback(self,ctx):
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        c=bdd.get_tokens_settings()[0]
        console.log(f"[ROULETTE] tirage_1 | {ctx.author} ({ctx.author.id})")
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        if u["tokens"] < 1:
            await ctx.send(f":information_source: Vous n'avez pas de jeton disponible. Allez en vocal, parlez dans le chat ou mettez {c['status']} en statut pour en gagner !",ephemeral=True)
            return
        items = bdd.get_roulette_items()
        if items == []:
            await ctx.send(":warning: Aucun item n'a été configuré, veuillez contacter un administrateur.",ephemeral=True)
            return
        rarity = [rar["rarity"] for rar in items]
        if ctx.author.id in opening:
            await ctx.send(":hourglass: Vous avez déjà un tirage en cours, veuillez attendre la fin de celui-ci.",ephemeral=True)
            return
        chosend_item = random.choices(items,weights=rarity)
        chosend_item = chosend_item[0]
        await ctx.send(f"Tirage en cours...",ephemeral=True)
        opening.append(ctx.author.id)
        # await asyncio.sleep(3)
        bdd.set_tokens(u["tokens"]-1,ctx.author.id)
        opening.remove(ctx.author.id)

        if chosend_item["type"] == "coins":
            bdd.set_coins(u["coins"]+chosend_item["data"],ctx.author.id)
            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} coins")
            await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} coins) !",ephemeral=True)
            await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {"{:,}".format(chosend_item['data'])} coins dans la roulette.")
        elif chosend_item["type"] == "jetons":
            bdd.set_tokens(u["tokens"]+chosend_item["data"],ctx.author.id)
            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} tokens")
            await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} jetons) !",ephemeral=True)
            await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {chosend_item['data']} jetons dans la roulette.")
        elif chosend_item["type"] == "role":
            r=ctx.guild.get_role(chosend_item["data"])
            if r is None:
                e=await generate_error_code(self.bot,f"Role {chosend_item['data']} does not exist | generated for {ctx.author} ({ctx.author.id})")
                await ctx.send(f":x: Le role {chosend_item['name']} n'existe plus, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{e}|| **il vous permettera de retirer votre gain** .",ephemeral=True)
                console.warning(f"[ROULETTE] Role {chosend_item['data']} does not exist")
                return
            if r in ctx.author.roles:  
                r = random.randint(100,1000)
                bdd.set_coins(u["coins"]+r,ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have role)")
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                await ctx.send(f":information_source: Vous avez déjà le role {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                return
            try:
                await ctx.author.add_role(r)
            except Exception as e:
                ee = await generate_error_code(self.bot,f"Failed to add role {chosend_item['data']} | Generated for {ctx.author} ({ctx.author.id}) \n . Error: {e}")
                console.warning(f"[ROULETTE] Failed to add role {chosend_item['data']} to {ctx.author} ({ctx.author.id}). Error: {e}")
                await ctx.send(f":x: Une erreur est survenue lors de l'ajout du role, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{ee}|| **il vous permettera de retirer votre gain** .",ephemeral=True)
                return
            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won role {chosend_item['data']}")
            await ctx.send(f":information_source:Vous avez gagné le role {chosend_item['name']} !",ephemeral=True)
            await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné le role '{chosend_item['name']}' dans la roulette.")  
        elif chosend_item["type"] == "badge":
            if u["badges"] == None:
                badges = []
            elif u["badges"] == "":
                badges = []
            else:
                if "," in str(u["badges"]):
                    badges = str(u["badges"]).split(",")
                else:
                    badges = [str(u["badges"])]
            if str(chosend_item["data"]) in badges:
                r = random.randint(100,1000)
                bdd.set_coins(u["coins"]+r,ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have badge)")
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                await ctx.send(f":information_source:Vous avez déjà le badge {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                return
            badges.append(str(chosend_item["data"]))
            if len(badges) > 1:
                badges = ",".join(badges)
            else:
                badges = badges[0]
            bdd.set_badges(badges,ctx.author.id)
            await ctx.send(f":tada: Vous avez gagné le badge {chosend_item['name']} !",ephemeral=True)
            await generate_log_embed(self.bot,f" <@{ctx.author.id}> a gagné le badge {chosend_item['name']} dans la roulette.")
            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won badge {chosend_item['data']}")
        
        elif chosend_item["type"] == "color":
            if u["colors"] == None:
                colors = []
            elif u["colors"] == "":
                colors = []
            else:
                if "," in str(u["colors"]):
                    colors = str(u["colors"]).split(",")
                else:
                    colors = [str(u["colors"])]
            if str(chosend_item["data"]) in colors:
                r = random.randint(100,1000)
                bdd.set_coins(u["coins"]+r,ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have color)")
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                await ctx.send(f":information_source:Vous avez déjà la couleur {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                return
            colors.append(str(chosend_item["data"]))
            if len(colors) > 1:
                colors = ",".join(colors)
            else:
                colors = colors[0]
            bdd.set_colors(colors,ctx.author.id)
            await ctx.send(f":tada: Vous avez gagné la couleur {chosend_item['name']} !",ephemeral=True)
            await generate_log_embed(self.bot,f" <@{ctx.author.id}> a gagné la couleur {chosend_item['name']} dans la roulette.")
            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won color {chosend_item['data']}")

        elif chosend_item["type"] == "nothing":
            await ctx.send("Vous n'avez rien gagné !",ephemeral=True)
            await generate_log_embed(self.bot,f"<@{ctx.author.id}> n'a rien gagné dans la roulette.")
            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won nothing")
        elif chosend_item["type"] == "pillages":
            await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {chosend_item['data']} pillages dans la roulette.")
            await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} pillage(s)) !",ephemeral=True)
            bdd.set_pillages(u["rob_availables"]+chosend_item["data"],ctx.author.id)
            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} pillages")
        else:
            await ctx.send(":x: Une erreur est survenue, veuillez contacter un administrateur.",ephemeral=True)
            console.alert(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won an unknown ({chosend_item['type']} {chosend_item['name']}) item")

    @component_callback("tirage_5")
    async def tirage_5_callback(self,ctx):
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        c=bdd.get_tokens_settings()[0]
        console.log(f"[ROULETTE] tirage_5 | {ctx.author} ({ctx.author.id})")
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        if u["tokens"] < 5:
            await ctx.send(f":information_source: Vous n'avez pas 5 jetons disponibles. Allez en vocal, parlez dans le chat ou mettez {c['status']} en statut pour en gagner.",ephemeral=True)
            return
        items = bdd.get_roulette_items()
        if items == []:
            await ctx.send(":warning: Aucun item n'a été configuré, veuillez contacter un administrateur.",ephemeral=True)
            return
        rarity = [rar["rarity"] for rar in items]
        if ctx.author.id in opening:
            await ctx.send(":hourglass: Vous avez déjà un tirage en cours, veuillez attendre la fin de celui-ci.",ephemeral=True)
            return
        r=random.randint(500,1500)
        bdd.set_coins(u["coins"]+r,ctx.author.id)
        u = bdd.check_user(ctx.author.id)[0]
        bdd.set_tokens(u["tokens"]-5,ctx.author.id)
        await ctx.send(f"5 Tirages en cours... \n Vous avez reçu {r} coins de bonus x5 !",ephemeral=True)
        opening.append(ctx.author.id)
        rrrr=[]
        for _ in range(5):
            await asyncio.sleep(1)
            u=bdd.check_user(ctx.author.id)
            u=u[0]
            chosend_item = random.choices(items,weights=rarity)
            chosend_item = chosend_item[0]
            if chosend_item["type"] == "coins":
                bdd.set_coins(u["coins"]+chosend_item["data"],ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} coins")
                rrrr.append(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} coins) !\n")
                await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} coins) !",ephemeral=True)
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {"{:,}".format(chosend_item['data'])} coins dans la roulette.")
            if chosend_item["type"] == "jetons":
                bdd.set_tokens(u["tokens"]+chosend_item["data"],ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} tokens")
                rrrr.append(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} jetons) !\n")
                await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} jetons) !",ephemeral=True)
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {chosend_item['data']} jetons dans la roulette.")
            if chosend_item["type"] == "role":
                r=ctx.guild.get_role(chosend_item["data"])
                if r is None:
                    e=await generate_error_code(self.bot,f"Role {chosend_item['data']} does not exist | generated for {ctx.author} ({ctx.author.id})")
                    rrrr.append(f":x: Le role {chosend_item['name']} n'existe plus, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{e}|| **il vous permettera de retirer votre gain** .\n")
                    await ctx.send(f":x: Le role {chosend_item['name']} n'existe plus, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{e}|| **il vous permettera de retirer votre gain** .",ephemeral=True)
                    console.warning(f"[ROULETTE] Role {chosend_item['data']} does not exist")
                else:
                    if r in ctx.author.roles:  
                        r = random.randint(100,1000)
                        bdd.set_coins(u["coins"]+r,ctx.author.id)
                        console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have role)")
                        await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                        rrrr.append(f":information_source: Vous avez déjà le role {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !\n")
                        await ctx.send(f":information_source: Vous avez déjà le role {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                    else:
                        try:
                            await ctx.author.add_role(r)
                            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won role {chosend_item['data']}")
                            rrrr.append(f":information_source:Vous avez gagné le role {chosend_item['name']} !\n")
                            await ctx.send(f":information_source:Vous avez gagné le role {chosend_item['name']} !",ephemeral=True)
                            await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné le role '{chosend_item['name']}' dans la roulette.")
                        except Exception as e:
                            ee = await generate_error_code(self.bot,f"Failed to add role {chosend_item['data']} | Generated for {ctx.author} ({ctx.author.id}) \n . Error: {e}")
                            console.warning(f"[ROULETTE] Failed to add role {chosend_item['data']} to {ctx.author} ({ctx.author.id}). Error: {e}")
                            rrrr.append(f":x: Une erreur est survenue lors de l'ajout du role, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{ee}|| **il vous permettera de retirer votre gain** .\n")
                            await ctx.send(f":x: Une erreur est survenue lors de l'ajout du role, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{ee}|| **il vous permettera de retirer votre gain** .",ephemeral=True)
            if chosend_item["type"] == "badge":
                if u["badges"] == None:
                    badges = []
                else:
                    if "," in str(u["badges"]):
                        badges = str(u["badges"]).split(",")
                    else:
                        badges = [str(u["badges"])]
                if str(chosend_item["data"]) in badges:
                    r = random.randint(100,1000)
                    bdd.set_coins(u["coins"]+r,ctx.author.id)
                    console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have badge)")
                    await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                    rrrr.append(f":information_source:Vous avez déjà le badge {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !\n")
                    await ctx.send(f":information_source:Vous avez déjà le badge {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                else:
                    badges.append(str(chosend_item["data"]))
                    if len(badges) > 1:
                        badges = ",".join(badges)
                    else:
                        badges = badges[0]
                    bdd.set_badges(badges,ctx.author.id)
                    rrrr.append(f":tada: Vous avez gagné le badge {chosend_item['name']} !\n")
                    await ctx.send(f":tada: Vous avez gagné le badge {chosend_item['name']} !",ephemeral=True)
                    await generate_log_embed(self.bot,f" <@{ctx.author.id}> a gagné le badge {chosend_item['name']} dans la roulette.")
                    console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won badge {chosend_item['data']}")
            if chosend_item["type"] == "color":
                if u["colors"] == None:
                    colors = []
                elif u["colors"] == "":
                    colors = []
                else:
                    if "," in str(u["colors"]):
                        colors = str(u["colors"]).split(",")
                    else:
                        colors = [str(u["colors"])]
                if str(chosend_item["data"]) in colors:
                    r = random.randint(100,1000)
                    bdd.set_coins(u["coins"]+r,ctx.author.id)
                    console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have color)")
                    await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                    rrrr.append(f":information_source:Vous avez déjà la couleur {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !\n")
                    await ctx.send(f":information_source:Vous avez déjà la couleur {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                else:
                    colors.append(str(chosend_item["data"]))
                    if len(colors) > 1:
                        colors = ",".join(colors)
                    else:
                        colors = colors[0]
                    bdd.set_colors(colors,ctx.author.id)
                    rrrr.append(f":tada: Vous avez gagné la couleur {chosend_item['name']} !\n")
                    await ctx.send(f":tada: Vous avez gagné la couleur {chosend_item['name']} !",ephemeral=True)
                    await generate_log_embed(self.bot,f" <@{ctx.author.id}> a gagné la couleur {chosend_item['name']} dans la roulette.")
                    console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won color {chosend_item['data']}")
            if chosend_item["type"] == "nothing":
                rrrr.append(f"Vous n'avez rien gagné !\n")
                await ctx.send("Vous n'avez rien gagné !",ephemeral=True)
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> n'a rien gagné dans la roulette.")
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won nothing")
            if chosend_item["type"] == "pillages":
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {chosend_item['data']} pillages dans la roulette.")
                rrrr.append(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} pillage(s)) !\n")
                await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} pillage(s)) !",ephemeral=True)
                bdd.set_pillages(u["rob_availables"]+chosend_item["data"],ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} pillages")
        bonus = random.randint(1000,3000)
        bdd.set_coins(u["coins"]+bonus,ctx.author.id)
        # await ctx.send(" ".join(rrrr),ephemeral=True)
        opening.remove(ctx.author.id)


    @component_callback("tirage_10")
    async def tirage_10_callback(self,ctx):
        await ctx.defer(ephemeral=True)
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        c=bdd.get_tokens_settings()[0]
        console.log(f"[ROULETTE] tirage_10 | {ctx.author} ({ctx.author.id})")
        if u == []:
            await ctx.send(":information_source: Vous n'avez pas de compte ! Créez en un en appuyant sur le bouton 'profil' !",ephemeral=True)
            return
        u = u[0]
        if u["tokens"] < 10:
            await ctx.send(f":information_source: Vous n'avez pas 10 jetons disponibles. Allez en vocal, parlez dans le chat ou mettez {c['status']} en statut pour en gagner.",ephemeral=True)
            return
        items = bdd.get_roulette_items()
        if items == []:
            await ctx.send(":warning: Aucun item n'a été configuré, veuillez contacter un administrateur.",ephemeral=True)
            return
        rarity = [rar["rarity"] for rar in items]
        if ctx.author.id in opening:
            await ctx.send(":hourglass: Vous avez déjà un tirage en cours, veuillez attendre la fin de celui-ci.",ephemeral=True)
            return
        r=random.randint(1000,3000)
        bdd.set_coins(u["coins"]+r,ctx.author.id)
        u = bdd.check_user(ctx.author.id)[0]
        bdd.set_tokens(u["tokens"]-10,ctx.author.id)
        await ctx.send(f"10 Tirages en cours... \n Vous avez reçu {r} coins de bonus x10 !",ephemeral=True)
        opening.append(ctx.author.id)
        rrrr=[]
        for _ in range(10):
            await asyncio.sleep(1)
            u=bdd.check_user(ctx.author.id)
            u=u[0]
            chosend_item = random.choices(items,weights=rarity)
            chosend_item = chosend_item[0]
            if chosend_item["type"] == "coins":
                bdd.set_coins(u["coins"]+chosend_item["data"],ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} coins")
                rrrr.append(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} coins) !\n")
                await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} coins) !",ephemeral=True)
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {"{:,}".format(chosend_item['data'])} coins dans la roulette.")
            if chosend_item["type"] == "jetons":
                bdd.set_tokens(u["tokens"]+chosend_item["data"],ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} tokens")
                rrrr.append(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} jetons) !\n")
                await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} jetons) !",ephemeral=True)
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {chosend_item['data']} jetons dans la roulette.")
            if chosend_item["type"] == "role":
                r=ctx.guild.get_role(chosend_item["data"])
                if r is None:
                    e=await generate_error_code(self.bot,f"Role {chosend_item['data']} does not exist | generated for {ctx.author} ({ctx.author.id})")
                    rrrr.append(f":x: Le role {chosend_item['name']} n'existe plus, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{e}|| **il vous permettera de retirer votre gain** .\n")
                    await ctx.send(f":x: Le role {chosend_item['name']} n'existe plus, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{e}|| **il vous permettera de retirer votre gain** .",ephemeral=True)
                    console.warning(f"[ROULETTE] Role {chosend_item['data']} does not exist")
                else:
                    if r in ctx.author.roles:  
                        r = random.randint(100,1000)
                        bdd.set_coins(u["coins"]+r,ctx.author.id)
                        console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have role)")
                        await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                        rrrr.append(f":information_source: Vous avez déjà le role {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !\n")
                        await ctx.send(f":information_source: Vous avez déjà le role {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                    else:
                        try:
                            await ctx.author.add_role(r)
                            console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won role {chosend_item['data']}")
                            rrrr.append(f":information_source:Vous avez gagné le role {chosend_item['name']} !\n")
                            await ctx.send(f":information_source:Vous avez gagné le role {chosend_item['name']} !",ephemeral=True)
                            await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné le role '{chosend_item['name']}' dans la roulette.")
                        except Exception as e:
                            ee = await generate_error_code(self.bot,f"Failed to add role {chosend_item['data']} | Generated for {ctx.author} ({ctx.author.id}) \n . Error: {e}")
                            console.warning(f"[ROULETTE] Failed to add role {chosend_item['data']} to {ctx.author} ({ctx.author.id}). Error: {e}")
                            rrrr.append(f":x: Une erreur est survenue lors de l'ajout du role, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{ee}|| **il vous permettera de retirer votre gain** .\n")
                            await ctx.send(f":x: Une erreur est survenue lors de l'ajout du role, veuillez contacter un administrateur et communiquez lui ce code **confidentiel** ||{ee}|| **il vous permettera de retirer votre gain** .",ephemeral=True)
            if chosend_item["type"] == "badge":
                if u["badges"] == None:
                    badges = []
                else:
                    if "," in str(u["badges"]):
                        badges = str(u["badges"]).split(",")
                    else:
                        badges = [str(u["badges"])]
                if str(chosend_item["data"]) in badges:
                    r = random.randint(100,1000)
                    bdd.set_coins(u["coins"]+r,ctx.author.id)
                    console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have badge)")
                    await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                    rrrr.append(f":information_source:Vous avez déjà le badge {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !\n")
                    await ctx.send(f":information_source:Vous avez déjà le badge {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                else:
                    badges.append(str(chosend_item["data"]))
                    if len(badges) > 1:
                        badges = ",".join(badges)
                    else:
                        badges = badges[0]
                    bdd.set_badges(badges,ctx.author.id)
                    rrrr.append(f":tada: Vous avez gagné le badge {chosend_item['name']} !\n")
                    await ctx.send(f":tada: Vous avez gagné le badge {chosend_item['name']} !",ephemeral=True)
                    await generate_log_embed(self.bot,f" <@{ctx.author.id}> a gagné le badge {chosend_item['name']} dans la roulette.")
                    console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won badge {chosend_item['data']}")
            if chosend_item["type"] == "color":
                if u["colors"] == None:
                    colors = []
                elif u["colors"] == "":
                    colors = []
                else:
                    if "," in str(u["colors"]):
                        colors = str(u["colors"]).split(",")
                    else:
                        colors = [str(u["colors"])]
                if str(chosend_item["data"]) in colors:
                    r = random.randint(100,1000)
                    bdd.set_coins(u["coins"]+r,ctx.author.id)
                    console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {r} coins (already have color)")
                    await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {r} coins dans la roulette.")
                    rrrr.append(f":information_source:Vous avez déjà la couleur {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !\n")
                    await ctx.send(f":information_source:Vous avez déjà la couleur {chosend_item['name']} ! \n Vous avez reçu un dédommagement de {r} coins !",ephemeral=True)
                else:
                    colors.append(str(chosend_item["data"]))
                    if len(colors) > 1:
                        colors = ",".join(colors)
                    else:
                        colors = colors[0]
                    bdd.set_colors(colors,ctx.author.id)
                    rrrr.append(f":tada: Vous avez gagné la couleur {chosend_item['name']} !\n")
                    await ctx.send(f":tada: Vous avez gagné la couleur {chosend_item['name']} !",ephemeral=True)
                    await generate_log_embed(self.bot,f" <@{ctx.author.id}> a gagné la couleur {chosend_item['name']} dans la roulette.")
                    console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won color {chosend_item['data']}")
            if chosend_item["type"] == "nothing":
                rrrr.append(f"Vous n'avez rien gagné !\n")
                await ctx.send("Vous n'avez rien gagné !",ephemeral=True)
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> n'a rien gagné dans la roulette.")
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won nothing")
            if chosend_item["type"] == "pillages":
                await generate_log_embed(self.bot,f"<@{ctx.author.id}> a gagné {chosend_item['data']} pillages dans la roulette.")
                rrrr.append(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} pillage(s)) !\n")
                await ctx.send(f":tada: Vous avez gagné {chosend_item['name']} ({chosend_item['data']} pillage(s)) !",ephemeral=True)
                bdd.set_pillages(u["rob_availables"]+chosend_item["data"],ctx.author.id)
                console.log(f"[ROULETTE] {ctx.author} ({ctx.author.id}) won {chosend_item['data']} pillages")
        bonus = random.randint(1000,3000)
        bdd.set_coins(u["coins"]+bonus,ctx.author.id)
        # await ctx.send(" ".join(rrrr),ephemeral=True)
        opening.remove(ctx.author.id)
