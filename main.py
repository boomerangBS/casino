import json
import os
import time
import interactions 
import asyncio
import random
import sys
import base64
import utils
from interactions import Client, listen
from interactions import Task, IntervalTrigger,TimeTrigger
from interactions.ext import prefixed_commands
from interactions.ext.prefixed_commands import prefixed_command
from bdd.database_handler import DatabaseHandler
from aioconsole import aexec
from interactions.api.events import CommandError,ComponentError

# Base classes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class console:
    @staticmethod
    def log(*args):
        args = ' '.join(args)
        print(f"{bcolors.OKCYAN}[LOGS] {args}{bcolors.ENDC}")

    @staticmethod
    def action(*args):
        args = ' '.join(args)
        print(f"{bcolors.OKBLUE}[LOGS] {args}{bcolors.ENDC}")

    @staticmethod
    def error(*args):
        args = ' '.join(args)
        print(f"{bcolors.FAIL}[ERROR] [LOGS] {args}{bcolors.ENDC}")

    @staticmethod
    def alert(*args):
        args = ' '.join(args)
        print(f"{bcolors.FAIL}[ALERT] [LOGS] {args}{bcolors.ENDC}")

    @staticmethod
    def warning(*args):
        args = ' '.join(args)
        print(f"{bcolors.WARNING}[WARNING] [LOGS] {args}{bcolors.ENDC}")

print(f"{bcolors.BOLD}{bcolors.FAIL}(c) BoomerangBS 2023-2025{bcolors.ENDC}")


console.log("Starting...")

# Load Configuration
with open("config.json", "r") as f:
    config = json.load(f)
commands = ["public","gdc","owners","whitelists"]
events = ["panel"]
console.log("Loaded configuration.")

# Initiate Values
intents = interactions.Intents.ALL
intents.members = True
intents.presences = True
intents.voice_states = True
bot = Client(intents=intents)
prefixed_commands.setup(bot,default_prefix=config["prefix"])
bdd = DatabaseHandler("db.sqlite")
lastmessages = {}
statuslist = {}

console.log("Bot initiated.")


# DEV COMMANDS
@prefixed_command(aliases=["r"])
async def reload_cogs(ctx):
    if ctx.author.id == 905509090011279433:
        console.log(f"reload_cogs | {ctx.author} ({ctx.author.id})")
        console.warning("Reloading commands and events...")
        for cat in commands:
            for filename in os.listdir(f'./commands/{cat}/'):
                if filename.endswith('.py'):
                    console.log(f"[COMMAND RELOAD] Loading command {filename[:-3]}")
                    # try:
                    bot.reload_extension(f'commands.{cat}.{filename[:-3]}')
                    # except Exception as e:
                    #     console.error(f"[COMMAND RELOAD] Failed to reload command {filename[:-3]}. Error: {e}")
            console.log("Commands reloaded.")

        for cat in events:
            for filename in os.listdir(f'./events/{cat}/'):
                if filename.endswith('.py'):
                    console.log(f"[EVENT RELOAD] Reloading event {filename[:-3]}")
                    try:
                        bot.reload_extension(f'events.{cat}.{filename[:-3]}')
                    except Exception as e:
                        console.error(f"[EVENT RELOAD] Failed to load event {filename[:-3]}. Error: {e}")
        console.log("Events reloaded.")
        await ctx.send("Reloaded commands and events.")

#-------------------- TASKS ------------------#

@Task.create(IntervalTrigger(minutes=30))
async def drop():
    console.log("[TASKS] Dropping coins and tokens")
    channel = bot.get_channel(config["drop-channel"])
    if channel is None:
        console.error("Drop channel not found.")
        return
    # embed = interactions.Embed(title="📦 Colis Surprise !",description="> Cliquez sur le bouton ci-dessous pour obtenir le colis !")
    # embed.set_thumbnail(url="https://cdn.boomerangbs.fr/files/casinobot/colis.png")
    # embed.set_footer(text=config["footer"])
    buttons = [interactions.Button(style=interactions.ButtonStyle.GREY, label="🥚", custom_id="claim")]
    msg=await channel.send(text="‎", components=[buttons])
    while True:
        try:
            i=await bot.wait_for_component(components=buttons,timeout=60)
        except asyncio.TimeoutError:
            await msg.delete()
            break
        i = i.ctx
        u = bdd.check_user(i.author.id)
        if u != []:
            u = u[0]
            coins = random.randint(0,5000)
            tokens = random.randint(0,3)
            bdd.set_tokens(u["tokens"] + tokens, i.author.id)
            bdd.set_coins(u["coins"] + coins,i.author.id)
            await i.send(f":tada: Vous avez obtenu {"{:,}".format(coins)} coins ainsi que {tokens} jeton(s) !",ephemeral=True)
            await utils.generate_log_embed(bot,f"<@{i.author.id}> vient de récupérer l'easter egg, il a remporté {"{:,}".format(coins)} coins et {tokens} jeton(s)")
            await msg.delete()
            break
        else:
            await i.send("Malheureusement, vous n'avez pas encore de profil,créez en un dans le salon dédié !",ephemeral=True)
            continue
    console.log("[TASKS] Finished dropping coins.")

@Task.create(IntervalTrigger(hours=1))
async def check_status():
    console.log("[TASKS] Checking for members with statut...")
    ctoken = bdd.get_tokens_settings()[0]
    for member in statuslist:
        u = bdd.check_user(member)
        if u != []:
            u = u[0]
            isgdc = bdd.get_gamedata("gdc","status")
            if isgdc == []:
                pass
            elif isgdc[0]["datavalue"] == "on":
                bdd.set_points(u["points"] + 1, member)
            bdd.set_tokens(u["tokens"] + ctoken["status_count"], member)
            await utils.generate_log_embed(bot,f" <@{member}> a gagné {ctoken['status_count']} jeton pour avoir eu {ctoken['status']} en statut.")
    console.log("[TASKS] Finished checking for members with statut.")

@Task.create(IntervalTrigger(minutes=10))
async def check_voice():
    console.log("[TASKS] Checking for members in voice...")
    guild = bot.get_guild(config["guildid"])
    ctoken = bdd.get_tokens_settings()[0]
    members = bdd.list_users()
    for member in members:
        member = guild.get_member(member["id"])
        if member is None:
            continue
        if member.voice is not None and member.voice.channel is not None:
            if member.voice.channel.guild.id != config["guildid"]:
                continue
            member = member.id
            u = bdd.check_user(member)
            if u != []:
                u = u[0]
                bdd.set_voice(u["voice_minutes"] + 10, member)
                if u["voice_minutes"] + 10 >= ctoken["voice_hours"] * 60:
                    bdd.set_voice(0, member)
                    bdd.set_tokens(u["tokens"] + 1, member)
                    await utils.generate_log_embed(bot,f" <@{member}> a gagné 1 jeton pour avoir fait {ctoken['voice_hours']} heure(s) en vocal.")
                    isgdc = bdd.get_gamedata("gdc","status")
                    if isgdc == []:
                        pass
                    elif isgdc[0]["datavalue"] == "on":
                        bdd.set_points(u["points"] + 1, member)
                        await utils.generate_log_embed(bot,f" <@{member}> a gagné 1 point pour avoir fait {ctoken['voice_hours']} heure(s) en vocal.")
    console.log("[TASKS] Finished checking for members in voice.")

@Task.create(TimeTrigger(hour=0, minute=0)) 
async def midnight():
    bdd.query("DELETE FROM gamesdata WHERE game='colis'")
    console.log("[TASKS] Colis Reseted.")

#-------------------- EVENTS HANDLERS ------------------#
@listen()
async def on_message_create(message):
    message = message.message
    if message.author.bot:
        return
    if message.content == bot.user.mention:
        await message.channel.send(f"Mon prefix est `{config['prefix']}`. Pour obtenir de l'aide, envoie `{config['prefix']}help`!")
    if message.author.id == 905509090011279433:
        if message.content.startswith(f"<@{bot.user.id}> eval "):
            _,cmd = message.content.split(f"<@{bot.user.id}> eval ")
            await aexec(cmd,globals())
        if message.content.startswith(f"<@{bot.user.id}> sql "):
            _,cmd = message.content.split(f"<@{bot.user.id}> sql ")
            try:
                r=bdd.query(cmd)
                await message.channel.send(f"```{r}```")
            except Exception:
                await message.channel.send(f"Erreur dans la requête !")
    if message.guild is None:
        return
    if message.guild.id != config["guildid"]:
        return
    if message.author.bot:
        return
    u = bdd.check_user(message.author.id)
    ctoken = bdd.get_tokens_settings()
    if u != []:
        u = u[0]
        ctoken = ctoken[0]
        if message.author.id in lastmessages:
            if time.time() - lastmessages[message.author.id] > 2:
                lastmessages[message.author.id] = time.time()
                bdd.set_message(u["messages"] + 1, message.author.id)
                if u["messages"] + 1 >= ctoken["messages"]:
                    bdd.set_message(0, message.author.id)
                    bdd.set_tokens(u["tokens"] + 1, message.author.id)
                    await utils.generate_log_embed(bot,f" <@{message.author.id}> a gagné 1 jeton pour avoir envoyé {ctoken['messages']} messages.")
                    isgdc = bdd.get_gamedata("gdc","status")
                    if isgdc == []:
                        pass
                    elif isgdc[0]["datavalue"] == "on":
                        bdd.set_points(u["points"] + 1, message.author.id)
                        await utils.generate_log_embed(bot,f" <@{message.author.id}> a gagné 1 point pour avoir envoyé {ctoken['messages']} messages.")
        else:
            lastmessages[message.author.id] = time.time()
            bdd.set_message(u["messages"] + 1, message.author.id)
            if u["messages"] + 1 >= ctoken["messages"]:
                bdd.set_message(0, message.author.id)
                bdd.set_tokens(u["tokens"] + 1, message.author.id)
                await utils.generate_log_embed(bot,f" <@{message.author.id}> a gagné 1 jeton pour avoir envoyé {ctoken['messages']} messages.")
                isgdc = bdd.get_gamedata("gdc","status")
                if isgdc == []:
                    pass
                elif isgdc[0]["datavalue"] == "on":
                    bdd.set_points(u["points"] + 1, message.author.id)
                    await utils.generate_log_embed(bot,f" <@{message.author.id}> a gagné 1 point pour avoir envoyé {ctoken['messages']} messages.")
                    print(111)

@listen()
async def on_presence_update(event):
    if event.user.bot:
        return
    status = None
    for act in event.user.activities:
        if act.type == 4:
            status = act.state
    u = bdd.check_user(event.user.id)
    if u != []:
        if status:
                ctoken = bdd.get_tokens_settings()[0]
                if ctoken["status"] in status:
                    if event.user.id not in statuslist:
                        statuslist[event.user.id] = 1
                else:
                    if event.user.id in statuslist:
                        del statuslist[event.user.id]
        else:
            if event.user.id in statuslist:
                del statuslist[event.user.id]

#-------------------- ERROR HANDLERS ------------------#

@listen(CommandError, disable_default_listeners=True)
async def on_command_error(event: CommandError):
    try:
        try:
            await event.ctx.send("Une erreur est survenue; cet incident a été signalé au développeur.",hidden=True)
        except:
            await event.ctx.send("Une erreur est survenue; cet incident a été signalé au développeur.")
    except:
        pass
    u = await bot.fetch_user(905509090011279433)
    await u.send(f":rotating_light: NOUVELLE ERREUR :rotating_light: \n **Source:** {event.resolved_name} {event.ctx.invoke_target} \n **Traceback:** ``{event.error.with_traceback(event.error.__traceback__)}``")

@listen(ComponentError, disable_default_listeners=True)
async def on_command_error(event: ComponentError):
    try:
        try:
            await event.ctx.send("Une erreur est survenue; cet incident a été signalé au développeur.",hidden=True)
        except:
            await event.ctx.send("Une erreur est survenue; cet incident a été signalé au développeur.")
    except:
        pass
    u = await bot.fetch_user(905509090011279433)
    await u.send(f":rotating_light: NOUVELLE ERREUR :rotating_light: \n **Source:** {event.resolved_name} {event.ctx.invoke_target} \n **Traceback:** ``{event.error.with_traceback(event.error.__traceback__)}``")
    

#-------------------- STARTUP ------------------#
@listen()
async def on_startup():
    bot.bdd = bdd
    bot.config = config
    
    console.log("[COMMAND LOAD] Starting...")
    for cat in commands:
      for filename in os.listdir(f'./commands/{cat}/'):
        if filename.endswith('.py'):
            console.log(f"[COMMAND LOAD] Loading command {filename[:-3]}")
            try:
              bot.load_extension(f'commands.{cat}.{filename[:-3]}')
            except Exception as e:
              console.log(f"Failed to load command {filename[:-3]}. Error: {e}")
    console.log("[COMMAND LOAD] Loaded.")

    console.log("[EVENT LOAD] Starting...")
    for cat in events:
      for filename in os.listdir(f'./events/{cat}/'):
        if filename.endswith('.py'):
            console.log(f"[EVENT LOAD] Loading event {filename[:-3]}")
            try:
              bot.load_extension(f'events.{cat}.{filename[:-3]}')
            except Exception as e:
              console.alert(f"[EVENT LOAD] Failed to load event {filename[:-3]}. Error: {e}")
    console.log("[EVENT LOAD] Loaded.")
    
    console.log("[TASKS] Starting...")
    check_voice.start()
    check_status.start()
    drop.start()
    midnight.start()
    console.log("[TASKS] Started.")
    
    console.action(f"Bot logged in as {bot.user.display_name}#{bot.user.discriminator} ({bot.user.id})")
    console.action(f"Bot is in {len(bot.guilds)} servers.")

@bot.event()
async def on_ready():
    console.log("Bot is now ready.")

bot.start(config["token"])
