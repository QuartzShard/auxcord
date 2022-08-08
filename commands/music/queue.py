## Initialisation
import boilerBot.lib as lib
import discord

from discord.ext import commands, tasks
from common import Player

## Define command cog
class queue(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Shows the current queue"
        self.usage = f"""
        {self.bot.command_prefix}queue
        {self.bot.command_prefix}queue <page number>
        """
        self.forbidden = False
        
    @commands.command()
    async def queue(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        if not guildVars["player"]:
            embed = lib.embed(
                title="ERROR",
                description="No queue to show",
                color = lib.errorColour
            )    
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        if command:
            page = int(command[0])
        else:
            page = 1
        q = guildVars["player"].queue
        qlist = ""
        qlen = len(q)
        if qlen > 20 and qlen >= 20*page:
            qlen = (20 * page)
            qlow = qlen - 20
        elif qlen > 20:
            qlow = 20 * (page - 1) 
        else:
            qlow = 0
        for i in range(qlow, qlen):
            qlist += f"{i+1}: {q[i].title}\n"
        embed = lib.embed(
            title = "Current queue:",
            description = qlist,
            footer = f"Page {page} of {len(q)//20 + 1}"
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
        return

    
        
    
def setup(bot):
    bot.add_cog(queue(bot))