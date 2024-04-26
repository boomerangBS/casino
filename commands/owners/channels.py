#ALLOW COMMAND
#allow commands <channel>

import interactions,random
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
from utils import console

class Allow(Extension):
    def __init__(self, bot):
        self.bot = bot
        
    @prefixed_command()
    async def commands(self, ctx,arg=None,channel=None):
        bdd=self.bot.bdd
        if channel:
            try:
                channel = int(channel)
            except:
                try:
                    channel = int(channel.split("<#")[1].split(">")[0])
                except:
                    await ctx.reply("Salon invalide !")
                    return
        else:
            channel = ctx.channel.id
        if arg == "add":
            bdd=self.bot.bdd
            d=bdd.get_gamedata("allowed_channels","channel")
            if d == []:
                bdd.add_gamedata("allowed_channels","channel","[]")
            if d == "":
                bdd.set_gamedata("allowed_channels","channel","[]")
                d="[]"
            d=bdd.get_gamedata("allowed_channels","channel")
            #str to list
            d=eval(d[0]["datavalue"])
            if channel in d:
                await ctx.reply("Ce salon est déjà autorisé !")
                return
            d.append(channel)
            bdd.set_gamedata("allowed_channels","channel",str(d))
            await ctx.reply("Salon autorisé !")
            console.log(f"commands casino allow | {ctx.author} ({ctx.author.id}) | {channel}")
        elif arg == "del":
            bdd=self.bot.bdd
            d=bdd.get_gamedata("allowed_channels","channel")
            if d == []:
                bdd.add_gamedata("allowed_channels","channel","[]")
            if d == "":
                bdd.set_gamedata("allowed_channels","channel","[]")
                d="[]"
            d=bdd.get_gamedata("allowed_channels","channel")
            #str to list
            d=eval(d[0]["datavalue"])
            if channel not in d:
                await ctx.reply("Ce salon n'est pas autorisé !")
                return
            d.remove(channel)
            bdd.set_gamedata("allowed_channels","channel",str(d))
            await ctx.reply("Salon retiré !")
            console.log(f"commands casino allow | {ctx.author} ({ctx.author.id}) | {channel}")
        else:
            await ctx.reply("Vous devez spécifier `add` ou `del` !")
            return

