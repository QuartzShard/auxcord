## Initialisation
import boilerBot.lib as lib
import nextcord

from  nextcord.ext import commands, tasks
from common import Player

## Define command cog
class queue(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Show the current queue"
        self.usage = f"""
        {self.bot.command_prefix}queue
        {self.bot.command_prefix}queue <page number>
        """
        self.hidden = False
        
    @nextcord.slash_command()
    async def queue(self, ctx, page=1):
        """Show the current queue

        Parameters
         ----------
        ctx: Interaction
            The interaction object
        page: int
            For queues longer than 20 tracks, show the specified page
        """
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        if not guildVars["player"]:
            embed = lib.embed(
                title="No queue to show",
                color = lib.errorColour
            )    
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
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