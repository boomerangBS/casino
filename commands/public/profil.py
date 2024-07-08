import interactions
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class Profil(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command(aliases=["bal"])
    async def profil(self, ctx,user=None):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
        bdd = self.bot.bdd
        u=bdd.check_user(ctx.author.id)
        if user:
            try:
                user = int(user)
            except:
                try:
                    user = int(user.split("<@")[1].split(">")[0])
                except:
                    pass
            if user:
                uu=bdd.check_user(user)
                if uu != []:
                    uu = uu[0]
                    if uu['clan'] == None:
                        uu['clan'] = "Aucun clan"
                    else:
                        clan = bdd.check_clan(uu['clan'])
                        if clan != []:
                            clan = clan[0]
                            uu['clan'] = clan["name"]
                        else:
                            uu['clan'] = "Clan inconnu"
                    s=bdd.get_tokens_settings()[0]
                    messages = s["messages"]-uu["messages"]
                    voice = s["voice_hours"]*60-uu["voice_minutes"]
                    userp = ctx.guild.get_member(user)
                    if userp == None:
                        display_name = "Utilisateur ayant quitté le serveur"
                        avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
                    else:
                        avatar_url = userp.avatar.url
                        display_name = userp.display_name
                    embed = interactions.Embed(description=f"**__Profil de {display_name}__**\n\n:trophy: `Point(s)` ➟ **{uu['points']}**\n:tickets: `Jeton(s)` ➟ **{uu['tokens']}**\n:crossed_swords: `Pillage(s) disponible(s)` ➟ **{uu['rob_availables']}**\n:coin: `Nombre de coins` ➟ **{"{:,}".format(uu['coins'])}**\n:beginner: `Clan` ➟ **{uu['clan']}**\n:incoming_envelope: `Messages restants`➟ **{messages} messages**\n:loud_sound: `Minutes de vocal restantes` ➟ **{voice} minutes**")
                    embed.set_footer(text=self.bot.config['footer'])
                    if avatar_url is not None:
                        embed.set_thumbnail(url=avatar_url)
                    else:
                        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
                    await ctx.reply(embed=embed,ephemeral=True)
                    return
                else:
                    await ctx.reply("Cet utilisateur n'a pas de profil !",ephemeral=True)
                    return
                
        if u == []:
            await ctx.reply("Vous n'avez pas de profil !",ephemeral=True)
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
            await ctx.reply(embed=embed,ephemeral=True)