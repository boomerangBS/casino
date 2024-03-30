import json,os
import discord #upm package(discord.py==1.7.3)
from discord.ext import commands, tasks
import discord_slash #upm package(discord-py-slash-command==3.0.3)
from discord_slash import ButtonStyle,SlashCommand 
from discord_slash.utils.manage_components import wait_for_component,create_actionrow,create_button
from discord_slash.utils.manage_commands import create_option,create_choice
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


cogs: list = ["cogs.ping","cogs.troll"]

#Load Config
f = open("config.json","r")
config = json.load(f)
f.close()

console.log("Loaded configuration.")

intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(command_prefix=config["prefix"], description="Base Bot AllBot Technologies (boomerangbs)")
# slash = SlashCommand(bot,sync_commands=True)
# Remove default help command :)
bot.remove_command('help')

console.log("Bot initiated.")

@bot.command()
async def ping(ctx):
  await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.event
async def on_ready():
  # for filename in os.listdir('./cogs'):
  #   if filename.endswith('.py'):
  #       print(f"{bcolors.OKBLUE}Loading cog {filename[:-3]}{bcolors.ENDC}")
  #       try:
  #         bot.load_extension(f'cogs.{filename[:-3]}')
  #         print(f"{bcolors.OKGREEN}Loaded cog {filename[:-3]}{bcolors.ENDC}")
  #       except Exception as e:
  #         exc = "{}: {}".format(type(e).__name__, e)
  #         print("Failed to load cog {}\n{}".format(filename[:-3], exc))

  print(f"{bcolors.OKGREEN}[LOGS] Bot logged in as {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
  print(f"{bcolors.OKGREEN}[LOGS] Bot is in {len(bot.guilds)} servers.")
  print(f"{bcolors.OKGREEN}[LOGS] Bot is in {len(bot.users)} users.{bcolors.ENDC}")
  console.log("Bot is ready.")

bot.run(config["token"])
  