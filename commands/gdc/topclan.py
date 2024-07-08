#COMMAND TOPCLAN
#affiche le top des clans ayant le plus de points

import interactions,math
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from interactions import Button, ButtonStyle


class TopClan(Extension):
    def __init__(self, bot):
        self.bot = bot

    @prefixed_command()
    async def topclan(self, ctx):
        check = self.bot.bdd.get_gamedata("allowed_channels","channel")
        bdd=self.bot.bdd
        status=bdd.get_gamedata("gdc","status")
        channel=bdd.get_gamedata("gdc","channel")
        if status == []:
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if status[0]["datavalue"] == "off":
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if channel == []:
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if channel[0]["datavalue"] == "NO":
            await ctx.reply("La guerre des clans n'est pas en cours !")
            return
        if ctx.channel.id != int(channel[0]["datavalue"]):
            await ctx.reply(f"Cette commande est uniquement utilisable dans <#{channel[0]["datavalue"]}>")
            return
        if check != []:
            check = eval(check[0]["datavalue"])
            if check != "":
                if ctx.channel.id not in check:
                    channels=[f"<#{i}>" for i in check]
                    await ctx.reply(f"Cette commande n'est pas autorisée dans ce salon ! Allez dans {",".join(channels)}.")
                    return
                bdd=self.bot.bdd
        clans = bdd.get_clans()
        clanspoint = []
        if clans == []:
            await ctx.reply("Aucun clan !")
            return
        for clan in clans:
            members = bdd.get_users_in_clan(clan["id"])
            points = 0
            for member in members:
                points += member["points"]
            clan["points"] = points
            clanspoint.append(clan)

        clans = sorted(clanspoint, key=lambda x: x["points"], reverse=True)
        description="Voici le classement des clans avec le plus de points."
        for i in range(10):
            try:
                clan = clans[i]
                if i+1 == 1:
                    description += f"\n\n🥇 {clan['name']} ({clan['id']}) - {"{:,}".format(clan['points'])} :coin:"
                elif i+1 == 2:
                    description += f"\n🥈 {clan['name']} ({clan['id']}) - {"{:,}".format(clan['points'])} :coin:"
                elif i+1 == 3:
                    description += f"\n🥉 {clan['name']} ({clan['id']}) - {"{:,}".format(clan['points'])} :coin:"
                else:
                    description += f"\n{i+1}. {clan['name']} ({clan['id']}) - {u"{:,}".format(clan['points'])} :coin:"
            except:
                break
        embed = interactions.Embed(title="🏆 Leaderboard",description=description)
        embed.set_footer(text=self.bot.config["footer"])
        i=1
        maxpages = math.ceil(len(clans) / 10)
        # await ctx.reply(embed=embed)
        arrows = [Button(style=ButtonStyle.PRIMARY, label="◀️", custom_id="prev"), Button(style=ButtonStyle.PRIMARY, label="▶️", custom_id="next")]
        c=await ctx.reply(embed=embed,components=[arrows])
        while True:
            try:
                iii=await self.bot.wait_for_component(components=arrows,timeout=200,check=lambda iii: iii.ctx.author.id == ctx.author.id and iii.ctx.message.id == c.id)
            except:
                await c.edit(components=[])
                return
            if iii.ctx.custom_id == "prev":
                if i == 1:
                    i = maxpages
                else:
                    i -= 1
            else:
                if i == maxpages:
                    i = 1
                else:
                    i += 1
            description="Voici le classement des clans avec le plus de points."
            if i == 1:
                for ii in range(10):
                    try:
                        clan = clans[ii]
                        if ii+1 == 1:
                            description += f"\n\n🥇 {clan['name']} ({clan['id']}) - {"{:,}".format(clan['points'])} :coin:"
                        elif ii+1 == 2:
                            description += f"\n🥈 {clan['name']} ({clan['id']}) - {"{:,}".format(clan['points'])} :coin:"
                        elif ii+1 == 3:
                            description += f"\n🥉 {clan['name']} ({clan['id']}) - {"{:,}".format(clan['points'])} :coin:"
                        else:
                            description += f"\n{ii+1}. {clan['name']} ({clan['id']}) - {u"{:,}".format(clan['points'])} :coin:"
                    except:
                        continue
                embed = interactions.Embed(title="🏆 Leaderboard",description=description)
                embed.set_footer(text=self.bot.config["footer"])
                await iii.ctx.edit_origin(embed=embed,components=[arrows])
                await c.edit(embed=embed,components=[arrows])
            else:
                for ii in range(1,11):
                    try:
                        clan = clans[ii+(i-1)*10]
                        description += f"\n{ii+(i-1)*10}. {clan['name']} ({clan['id']}) - {u"{:,}".format(clan['points'])} :coin:"
                    except:
                        continue
                embed = interactions.Embed(title="🏆 Leaderboard",description=description)
                embed.set_footer(text=self.bot.config["footer"])
                await iii.ctx.edit_origin(embed=embed,components=[arrows])