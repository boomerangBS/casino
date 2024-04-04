import json
import os
import math
import time
import interactions

from interactions import Client, listen, component_callback
from interactions import slash_command, SlashContext
from interactions import slash_option,OptionType,SlashCommandChoice,User,Button, ButtonStyle
from interactions import Task, IntervalTrigger
from interactions.ext import prefixed_commands
from interactions.ext.prefixed_commands import prefixed_command

from bdd.database_handler import DatabaseHandler

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

print(f"{bcolors.BOLD}{bcolors.FAIL}(c) BoomerangBS 2023{bcolors.ENDC}")
console.log("Starting...")

# Load Config
with open("config.json", "r") as f:
    config = json.load(f)
category = ["public","owners"]
console.log("Loaded configuration.")

intents = interactions.Intents.ALL
intents.members = True
intents.presences = True
intents.voice_states = True
bot = Client(intents=intents)
prefixed_commands.setup(bot,default_prefix=config["prefix"])
bdd = DatabaseHandler("db.sqlite")
console.log("Bot initiated.")
lastmessages = {}
statuslist = {}


# DEV COMMANDS
@prefixed_command(aliases=["r"])
async def reload_cogs(ctx):
    if ctx.author.id == 905509090011279433:
        for cat in category:
            for filename in os.listdir(f'./cogs/{cat}/'):
                if filename.endswith('.py'):
                    print(f"{bcolors.OKBLUE}Reloading cog {filename[:-3]}{bcolors.ENDC}")
                    try:
                        bot.reload_extension(f'cogs.{cat}.{filename[:-3]}')
                        print(f"{bcolors.OKGREEN}Reloaded cog {filename[:-3]}{bcolors.ENDC}")
                    except Exception as e:
                        exc = "{}: {}".format(type(e).__name__, e)
                        print("Failed to reload cog {}\n{}".format(filename[:-3], exc))
        await ctx.send("Reloaded cogs.")

# REWARD EVENTS

@Task.create(IntervalTrigger(hours=1))
async def check_status():
    ctoken = bdd.get_tokens_settings()[0]
    for member in statuslist:
        u = bdd.check_user(member)
        if u != []:
            u = u[0]
            bdd.set_tokens(u["tokens"] + ctoken["status_count"], member)

@Task.create(IntervalTrigger(minutes=10))
async def check_voice():
    guild = bot.get_guild(config["guildid"])
    ctoken = bdd.get_tokens_settings()[0]

    for vc in guild.voice_channels:
        member_ids = list(vc.voice_states.keys())
        for member in member_ids:
            u = bdd.check_user(member)
            if u != []:
                u = u[0]
                bdd.set_voice(u["voice_minutes"] + 10, member)
                if u["voice_minutes"] + 10 >= ctoken["voice_hours"] * 60:
                    bdd.set_voice(0, member)
                    bdd.set_tokens(u["tokens"] + 1, member)
                    bdd.set_points(u["points"] + 1, member)

@listen()
async def on_message_create(message):
    message = message.message
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
                    bdd.set_points(u["points"] + 1, message.author.id)
        else:
            lastmessages[message.author.id] = time.time()
            bdd.set_message(u["messages"] + 1, message.author.id)
            if u["messages"] + 1 >= ctoken["messages"]:
                bdd.set_message(0, message.author.id)
                bdd.set_tokens(u["tokens"] + 1, message.author.id)
                bdd.set_points(u["points"] + 1, message.author.id)

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


# SYSTEM EVENTS

@listen()
async def on_startup():
    bot.bdd = bdd
    bot.config = config
    for cat in category:
      for filename in os.listdir(f'./cogs/{cat}/'):
        if filename.endswith('.py'):
            print(f"{bcolors.OKBLUE}Loading cog {filename[:-3]}{bcolors.ENDC}")
            try:
              bot.load_extension(f'cogs.{cat}.{filename[:-3]}')
            except Exception as e:
              print(f"Failed to load extension {filename[:-3]}. Error: {e}")

    console.log("Cogs loaded.")
    console.log("Starting Tasks...")
    check_voice.start()
    check_status.start()
    console.log("Tasks started.")
    print(f"{bcolors.OKGREEN}[LOGS] Bot logged in as {bot.user.display_name}#{bot.user.discriminator} ({bot.user.id})")
    print(f"{bcolors.OKGREEN}[LOGS] Bot is in {len(bot.guilds)} servers.{bcolors.ENDC}")

@bot.event()
async def on_ready():
    console.log("Bot is now ready.")

bot.start(config["token"])
