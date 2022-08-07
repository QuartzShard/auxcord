## Initialisation
import boilerBot.lib as lib
import discord

from discord.ext import commands, tasks
from common import Player

## Define command cog
class skip(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Skip the current track"
        self.usage = f"""
        {self.bot.command_prefix}skip
        """
        self.forbidden = False
        
    @commands.command()
    async def skip(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        if not guildVars["player"]:
            embed = lib.embed(
                title="Not playing anything",
                color = lib.errorColour
            )    
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        title = guildVars["player"].queue[0].title
        guildVars["player"].voiceclient.stop()
        lib.set(ctx.guild.id, self.bot, guildVars)
        embed=lib.embed(
            title=f"Skipped {title}"
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
        return

    
        
    
def setup(bot):
    bot.add_cog(skip(bot))
