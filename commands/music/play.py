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
        self.forbidden = False
        
    @commands.command()
    async def play(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        # No track specified, figure out if resuming
        if len(command) == 0:
            if ctx.voice_client != None:
                if ctx.voice_client.is_paused():
                    ctx.voice_client.resume()
                    embed = lib.embed(
                        title = 'Playback has been resumed.'
                    )
                    await ctx.send(embed=embed)
                    return
            embed = lib.embed(
                title = 'ERROR',
                description = 'You did not specify what to play.',
                color = lib.errorColor
            )
            await ctx.send(embed=embed)
            return
        # Join channel if not already in one
        elif not ctx.me.voice:
            guildVars["player"] = Player(ctx.guild, ctx)
            await guildVars["player"].connect(ctx.author.voice.channel)
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            embed = lib.embed(
                title = "You must be in the same voice channel as the bot to play"
            )
            await ctx.send(embed=embed)
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
        if type(media) == Track:
            track = media
        else:
            track = Track()
            await track._init(media, self.bot, guild)
        if track.restricted:
            embed = lib.embed(
                title = "Playback error. Likely age restricted or otherwise prohibited video",
                color = lib.errorColour
            )
            await ctx.send(embed=embed)
            return
        guildVars["player"].addtoqueue(track)
        embed = await track.play(guildVars["player"],guild,self.onFinish)
        await ctx.send(embed=embed)
        lib.set(guild.id,self.bot,guildVars)

    def onFinish(self, guild):
        guildVars = lib.retrieve(guild.id, self.bot)
        nexttrack = guildVars["player"].nexttrack()
        if not guild.me.voice:
            return
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