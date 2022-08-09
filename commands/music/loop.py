## Initialisation
import boilerBot.lib as lib
import discord

from discord.ext import commands, tasks
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
        
    @commands.command()
    async def loop(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        
        if not guildVars["player"]:
            embed = lib.embed(
                title = "ERROR",
                description = "No queue to loop.",
                color = lib.errorColour
            )    
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        guildVars["player"].loop = not guildVars["player"].loop    
        lib.set(ctx.guild.id,self.bot,guildVars)
        if guildVars["player"].loop:
            description = "Queue loop enabled."
        else:
            description = "Queue loop disabled."
        embed = lib.embed(
            title = "SUCCESS",
            description = description
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)    
        return

def setup(bot):
    bot.add_cog(loop(bot))