# HELP COMMAND 

import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from utils import console
from datetime import datetime,timedelta

class Help(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def help(self, ctx):
        console.log(f"help | {ctx.author} ({ctx.author.id})")
        prefix = self.bot.config["prefix"]
        help1 = interactions.Embed(title="📚 Public", description=f"""
            Voici la liste des commandes disponibles :
                                   
            - **{prefix}help** : Affiche la liste des commandes.
            - **{prefix}daily** : Récupère ses coins quotidiens toutes les 24 heures.
            - **{prefix}collect** : Collecte une récompense toutes les 20 minutes.
            - **{prefix}gift** : Une chance sur trois pour gagner tous les 20 minutes.
            - **{prefix}jackpot** : Tombe sur 777 pour devenir riche, 1,000 coins requis.
            - **{prefix}bingo** : Devine le numéro gagnant et gagne le pot, 250 coins requis.
            - **{prefix}don** : Donne des coins à quiconque, 10% de taxe.
            - **{prefix}rob** :  Vole les coins à un  utilisateur toutes les 20 minutes, pillage requis.
            - **{prefix}top** : Affiche le top 10 des utilisateurs les plus riches.""")
        help2 = interactions.Embed(title=":beginner: GDC", description=f"""
            Voici la liste des commandes disponibles :
                                   
            - **{prefix}pillage** : Pille des points à un utilisateur toutes les 20 minutes.
            - **{prefix}freepillage** : Pille des points un utilisateur gratuitement toutes les 2 heures. 
            - **{prefix}topclan** : Affiche le top 10 des clans les plus forts.
            - **{prefix}rank** : Affiche le top 10 des joueurs avec le plus de points. 
            - **{prefix}create** : Créé votre clan de 3 membres avec 5,000 coins requis. 
            - **{prefix}leave** : Quitte ton clan actuel. 
            - **{prefix}invite** : Le chef de clan peut inviter 2 membres. 
            - **{prefix}delete** : Supprime un clan, réservé au chef.
            - **{prefix}quetes** : Soon...""")
        help3 = interactions.Embed(title=":scroll: Whitelist", description=f"""
            Voici la liste des commandes disponibles :
                                   
            - **{prefix}add** : Ajoute Points/Pillages/Coins/Jetons à un utilisateur.
            - **{prefix}remove** : Retire Points/Pillages/Coins/Jetons à un utilisateur.
            - **{prefix}drop** : Envoie un colis rempli de coins/pillages/points/jetons.
            - **{prefix}bl** : Voir la liste des utilisateurs interdits.
            - **{prefix}bl <user>** : Ajoute/Retire un utilisateur de la blacklist.""")
        
        help4 = interactions.Embed(title="👑 Owner", description=f"""
            Voici la liste des commandes disponibles :
                                                  
            - **{prefix}setgains** : Définis les gains de jetons.
            - **{prefix}setgdc** : Configure et lance une guerre de clan.
            - **{prefix}setcategories** : Définis les catégories de la roulette. 
            - **{prefix}setitems** : Définis les items à gagner par catégorie de la roulette. 
            - **{prefix}setshop** : Configure les objets du shop achetables.
            - **{prefix}wl** : Visualise la liste de la Whitelist.
            - **{prefix}wl <user>** : Ajoute/Retire un utilisateur à la Whitelist.""")
        servername = "/lova en statut pour gagner des jetons."
        help1.set_footer(text=servername)
        help2.set_footer(text=servername)
        help3.set_footer(text=servername)
        help4.set_footer(text=servername)
        buttons = [
            interactions.Button(emoji=":arrow_backward:",custom_id="left",style=ButtonStyle.BLUE),
            interactions.Button(emoji=":arrow_forward:",custom_id="right",style=ButtonStyle.BLUE)
        ]
        m=await ctx.send(embed=help1,components=[buttons])
        page = 1
        def check(i):
            return i.ctx.author==ctx.author and i.ctx.message==m
        while True:
            try:
                i = await self.bot.wait_for_component(components=buttons,timeout=300,check=check)
            except asyncio.TimeoutError:
                await m.edit(components=[])
                break
            i = i.ctx
            if i.custom_id=="left":
                if page==1:
                    page=4
                else:
                    page-=1
            elif i.custom_id=="right":
                if page==4:
                    page=1
                else:
                    page+=1
            if page==1:
                await i.edit_origin(embed=help1)
            elif page==2:
                await i.edit_origin(embed=help2)
            elif page==3:
                await i.edit_origin(embed=help3)
            elif page==4:
                await i.edit_origin(embed=help4)
            else:
                await i.edit_origin(embed=help1)
