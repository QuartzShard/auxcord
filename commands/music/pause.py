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
        
    @commands.command()
    async def pause(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        if not ctx.me.voice or ctx.voice_client == None:
            embed = lib.embed(
                title = 'There is nothing currently playing',
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        elif ctx.author.voice.channel != ctx.me.voice.channel:
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
        ctx.voice_client.pause()
        guildVars['player'].ispaused = True
        embed = lib.embed(
            title = f'Playback has been paused, use {self.bot.command_prefix}play to resume'
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
    
def setup(bot):
    bot.add_cog(pause(bot))