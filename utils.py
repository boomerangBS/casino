import random,string,json
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
config = json.load(open('config.json'))
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
  
async def generate_error_code(bot,error_message:str):
  ecode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
  channel = bot.get_channel(config['error-logs-admin'])
  await channel.send(f" **ERREUR** \n Code : ||{ecode}|| \n Erreur : {error_message}")
  if channel is None:
    return "Erreur lors de la génération du code d'erreur."
  return ecode

