## Initialisation
import boilerBot.lib as lib
import nextcord

from  nextcord.ext import commands, tasks
from common import Player

## Define command cog
class loop(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Loops the current queue"
        self.usage = f"""
        {self.bot.command_prefix}loop
        """
        self.hidden = False
        
    @nextcord.slash_command()
    async def loop(self, ctx):
        """Loops the current queue.

        Parameters
        ----------
            ctx: Interaction
                The interaction object    
        """
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        
        if not guildVars["player"]:
            embed = lib.embed(
                title="No queue to loop",
                color = lib.errorColour
            )    
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        guildVars["player"].loop = not guildVars["player"].loop    
        lib.set(ctx.guild.id,self.bot,guildVars)
        if guildVars["player"].loop:
            title = "Queue loop enabled."
        else:
            title = "Queue loop disabled."
        embed = lib.embed(
            title = title
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)    
        return

    
        
    
def setup(bot):
    bot.add_cog(loop(bot))