## Initialisation
import boilerBot.lib as lib
import nextcord
import asyncio

from  nextcord.ext import commands, tasks

## Define command cog
class leave(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Leaves the current voice channel"
        self.usage = f"""
        {self.bot.command_prefix}leave
        """
        self.hidden = False
        
    @nextcord.slash_command()
    async def leave(self, ctx):
        """Leaves the current voice channel.
        
        Parameters
        ----------
            ctx: Interaction
                The interaction object
        """ 
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        if not guildVars['player']:
            return
        if ctx.user.voice.channel != guildVars['player'].voiceclient.channel:
            embed = lib.embed(
                title = "You must be in the same voice channel to disconnect the bot",
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        await guildVars['player'].voiceclient.disconnect()
        guildVars["player"] = None
        embed = lib.embed(
            title = f"Left **{ctx.user.voice.channel}**"
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        await asyncio.sleep(5)
        guildVars["previous"] = await lib.clean(guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
        return       

    
        
    
def setup(bot):
    bot.add_cog(leave(bot))