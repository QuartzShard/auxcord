## Initialisation
import boilerBot.lib as lib
import discord
import asyncio

from discord.ext import commands, tasks
from common import ytdlhandler, Track, Player

## Define command cog
class play(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Fetches audio from youtube to play in the current voice channel"
        self.usage = f"""
        {self.bot.command_prefix}play <search term>
        {self.bot.command_prefix}play <youtube_url>
        """
        self.hidden = False
        
    @commands.command()
    async def play(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        # No track specified, figure out if resuming
        if len(command) == 0:
            if ctx.voice_client != None:
                if guildVars['player'].ispaused:
                    ctx.voice_client.resume()
                    guildVars['player'].ispaused = False
                    embed = lib.embed(
                        title = 'Playback has been resumed.'
                    )
                    guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
                    lib.set(ctx.guild.id,self.bot,guildVars)
                    return
            embed = lib.embed(
                title = 'You did not specify what to play.',
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        # Join channel if not already in one
        elif not guildVars['player']:
            guildVars["player"] = Player(ctx.guild, ctx)
            if ctx.me.voice:
                guildVars['player'].voiceclient = ctx.voice_client
            else:
                await guildVars["player"].connect(ctx.author.voice.channel)
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            embed = lib.embed(
                title = "You must be in the same voice channel as the bot to play"
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        ## If more than one word is passed, collapse args into one string
        if len(command) > 1:
            media = " ".join(command)
        else:
            media = command[0]
        
        lib.set(ctx.guild.id,self.bot,guildVars)
        await self.playback(media,ctx.guild)
            
    async def playback(self,media,guild):   
        guildVars = lib.retrieve(guild.id, self.bot)
        ctx = guildVars["player"].ctx
        await ctx.channel.trigger_typing()
        if type(media) == Track:
            track = media
        else:
            track = Track(media)
            await track.async_init(self.bot.loop, guild)
        if track.restricted:
            embed = lib.embed(
                title = "Playback error. Likely age restricted or otherwise prohibited video",
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        embed = await track.play(self.bot,ctx,guildVars["player"],guild,self.onFinish)
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
        return

    def onFinish(self, guild):
        guildVars = lib.retrieve(guild.id, self.bot)
        if not guild.me.voice or not guildVars["player"]:
            return
        nexttrack = guildVars["player"].nexttrack()
        if not nexttrack:
            coroutine = guildVars["player"].voiceclient.disconnect()
        else:
            coroutine = self.playback(nexttrack, guild)
        lib.set(guild.id,self.bot,guildVars)
        future = asyncio.run_coroutine_threadsafe(coroutine, self.bot.loop)
        try:
            future.result()
        except Exception as er:
            print(er)
            pass



    
        
    
def setup(bot):
    bot.add_cog(play(bot))