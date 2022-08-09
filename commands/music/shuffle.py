## Initialisation
import boilerBot.lib as lib
import discord, random

from discord.ext import commands, tasks
from common import Player

## Define command cog
class shuffle(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Randomizes the order of the queue"
        self.usage = f"""
        {self.bot.command_prefix}shuffle
        """
        self.forbidden = False
        
    @commands.command()
    async def shuffle(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        if not guildVars["player"]:
            embed = lib.embed(
                title="ERROR",
                description="There is no queue to shuffle.",
                color = lib.errorColour
            )    
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            embed = lib.embed(
                title = "ERROR",
                description="You must be in the same voice channel as the bot to shuffle.",
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return      
        random.shuffle(guildVars["player"].queue)
        embed = lib.embed(
            title = "SUCCESS",
            description="The queue has been shuffled."
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
        return

    
        
    
def setup(bot):
    bot.add_cog(shuffle(bot))