## Initialisation
import boilerBot.lib as lib
import discord
import asyncio

from discord.ext import commands, tasks

## Define command cog
class leave(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Leaves a voice channel"
        self.usage = f"""
        {self.bot.command_prefix}leave
        """
        self.forbidden = False
        
    @commands.command()
    @commands.has_guild_permissions(connect=True)
    async def leave(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        if ctx.me.voice == None:
            return
        if ctx.author.voice.channel != ctx.me.voice.channel:
            embed = lib.embed(
                title = "You must be in the same voice channel to disconnect the bot",
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        guildVars["player"] = None
        await ctx.voice_client.disconnect()
        embed = lib.embed(
            title = f"Left **{ctx.me.voice.channel}**"
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        await asyncio.sleep(5)
        guildVars["previous"] = await lib.clean(guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
        return       

    
        
    
def setup(bot):
    bot.add_cog(leave(bot))