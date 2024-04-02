import json,os,math,time
import discord #upm package(discord.py==1.7.3)
from discord.ext import commands, tasks
import discord_slash #upm package(discord-py-slash-command==3.0.3)
from discord_slash import ButtonStyle,SlashCommand 
from discord_slash.utils.manage_components import wait_for_component,create_actionrow,create_button
from discord_slash.utils.manage_commands import create_option,create_choice
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
  def log(*args):
    args = ' '.join(args)
    print(f"{bcolors.OKCYAN}[LOGS] {args}{bcolors.ENDC}")
  def action(*args):
    args = ' '.join(args)
    print(f"{bcolors.OKBLUE}[LOGS] {args}{bcolors.ENDC}")
  def error(*args):
    args = ' '.join(args)
    print(f"{bcolors.FAIL}[ERROR] [LOGS] {args}{bcolors.ENDC}")
  def alert(*args):
    args = ' '.join(args)
    print(f"{bcolors.FAIL}[ALERT] [LOGS] {args}{bcolors.ENDC}")
  def warning(*args):
    args = ' '.join(args)
    print(f"{bcolors.WARNING}[WARNING] [LOGS] {args}{bcolors.ENDC}")


print(f"{bcolors.BOLD}{bcolors.FAIL}(c) BoomerangBS 2023{bcolors.ENDC}")
console.log("Starting...")



#Load Config
f = open("config.json","r")
config = json.load(f)
f.close()
category = ["public"]
console.log("Loaded configuration.")

intents = discord.Intents().all()
intents.members = True
intents.presences = True
intents.voice_states = True
intents
bot = commands.Bot(command_prefix=config["prefix"], description="BoomerangBSLEBG")
bdd = DatabaseHandler("db.sqlite")
# Remove default help command :)
bot.remove_command('help')
console.log("Bot initiated.")
lastmessages = {}

@tasks.loop(minutes=10)
async def check_voice():
  guild = bot.get_guild(config["guildid"])
  ctoken=bdd.get_tokens_settings()[0]

  for vc in guild.voice_channels:
    member_ids = list(vc.voice_states.keys())
    for member in member_ids:
      u=bdd.check_user(member)
      if u != []:
        u = u[0]
        bdd.set_voice(u["voice_minutes"]+10,member)
        if u["voice_minutes"]+10 >= ctoken["voice_hours"]*60:
          bdd.set_voice(0,member)
          bdd.set_tokens(u["tokens"]+1,member)
          bdd.set_points(u["points"]+1,member)



@bot.event
async def on_message(message):
  if message.guild == None:
    return
  if message.guild.id != config["guildid"]:
    return
  if message.author.bot:
    return
  u=bdd.check_user(message.author.id)
  ctoken=bdd.get_tokens_settings()
  if u != []:
    u = u[0]
    ctoken = ctoken[0]
    if message.author.id in lastmessages:
      if time.time() - lastmessages[message.author.id] > 2:
        lastmessages[message.author.id] = time.time()
        bdd.set_message(u["messages"]+1,message.author.id)
        if u["messages"]+1 >= ctoken["messages"]:
          bdd.set_message(0,message.author.id)
          bdd.set_tokens(u["tokens"]+1,message.author.id)
          bdd.set_points(u["points"]+1,message.author.id)
    else:
      lastmessages[message.author.id] = time.time()
      bdd.set_message(u["messages"]+1,message.author.id)
      if u["messages"]+1 >= ctoken["messages"]:
          bdd.set_message(0,message.author.id)
          bdd.set_tokens(u["tokens"]+1,message.author.id)
          bdd.set_points(u["points"]+1,message.author.id)
  await bot.process_commands(message)


# DEV COMMANDS
@bot.command(aliases=["r"])
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


# SYSTEM EVENTS
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    return
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(':warning: Il manque des arguments pour cette commande.')
    return
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.send(':warning: Commande en cooldown, reesayez dans {}s.'.format(math.ceil(error.retry_after)))
    return
  raise error

@bot.event
async def on_ready():
  bot.bdd = bdd
  bot.config = config
  for cat in category:
    for filename in os.listdir(f'./cogs/{cat}/'):
      if filename.endswith('.py'):
          print(f"{bcolors.OKBLUE}Loading cog {filename[:-3]}{bcolors.ENDC}")
          try:
            bot.load_extension(f'cogs.{cat}.{filename[:-3]}')
            print(f"{bcolors.OKGREEN}Loaded cog {filename[:-3]}{bcolors.ENDC}")
          except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(filename[:-3], exc))
  console.log("Cogs loaded.")
  console.log("Starting Tasks...")
  check_voice.start()
  console.log("Tasks started.")
  print(f"{bcolors.OKGREEN}[LOGS] Bot logged in as {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
  print(f"{bcolors.OKGREEN}[LOGS] Bot is in {len(bot.guilds)} servers.")
  print(f"{bcolors.OKGREEN}[LOGS] Bot is in {len(bot.users)} users.{bcolors.ENDC}")
  console.log("Bot is ready.")

bot.run(config["token"])
  