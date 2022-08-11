## Initialisation
import boilerBot.lib as lib
import nextcord, asyncio

from  nextcord.ext import commands, tasks
from common import ytdlhandler, Track, Player

## Define command cog
class pause(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Pauses current playback"
        self.usage = f"""
        {self.bot.command_prefix}pause
        """
        self.hidden = False
        
    @nextcord.slash_command()
    async def pause(self, ctx):
        """Pauses current playback.

        Parameters
        ----------
            ctx: Interaction
                The interaction object
        """
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        if not guildVars['player']:
            embed = lib.embed(
                title = 'There is nothing currently playing',
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        elif ctx.user.voice.channel != guildVars['player'].voiceclient.channel:
            embed = lib.embed(
                title = 'You must be in the same voice channel as the bot to pause',
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        elif guildVars['player'].ispaused:
            embed = lib.embed(
                title =  f'Already paused, use {self.bot.command_prefix}play to resume',
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        guildVars['player'].voiceclient.pause()
        guildVars['player'].ispaused = True
        embed = lib.embed(
            title = f'Playback has been paused, use {self.bot.command_prefix}play to resume'
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
    
def setup(bot):
    bot.add_cog(pause(bot))