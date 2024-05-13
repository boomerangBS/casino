import interactions, random, asyncio
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
isrool=[]
class roulette(Extension):
    def __init__(self, bot):
        self.bot = bot
    
    @prefixed_command(aliases=["rool","rl","rools"])
    async def roulette(ctx,mise=None,color=None):
        #! NOT IMPLEMENTED , DO NOT USE
        # TODO : Implement roulette command
        return