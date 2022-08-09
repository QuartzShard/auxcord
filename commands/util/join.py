## Initialisation
import boilerBot.lib as lib
import discord

from discord.ext import commands, tasks
from common import Player

## Define command cog
class join(commands.Cog):
    ## Initialise with help info
    def __init__(self,bot):
        self.bot = bot
        self.category = lib.getCategory(self.__module__)
        self.description = "Joins a voice channel"
        self.usage = f"""
        {self.bot.command_prefix}join
        """
        self.hidden = False
        
    @commands.command()
    @commands.has_guild_permissions(connect=True)
    async def join(self, ctx, *command):
        guildVars = lib.retrieve(ctx.guild.id, self.bot)
        # Check caller is in a voice channel
        if ctx.author.voice == None:
            embed = lib.embed(
                title = "You are not in a voice channel",
                description = "You must be in a voice channel for the bot to join you",
                color = lib.errorColour
            )
            guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
            lib.set(ctx.guild.id,self.bot,guildVars)
            return
        # Check bot is not already playing music, and if it is, check caller is allowed to move users
        if ctx.voice_client != None:
            if ctx.author.guild_permissions.move_members == False:
                embed = lib.embed(
                    title = "You are not permitted to move the bot",
                    description = 'Only users with the "Move Members" permission may move the bot',
                    color = lib.errorColour
                )
                guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
                lib.set(ctx.guild.id,self.bot,guildVars)
                return
            else:
                await guildVars["player"].voiceclient.move_to(ctx.author.voice.channel)
        else:
            guildVars["player"] = Player(ctx.guild, ctx)
            await guildVars["player"].connect(ctx.author.voice.channel)
        embed = lib.embed(
            title = f"Joined **{ctx.author.voice.channel}**",
            color = lib.defaultColour
        )
        guildVars["previous"] = await lib.send(ctx,embed,guildVars["previous"])
        lib.set(ctx.guild.id,self.bot,guildVars)
        return

    
        
    
def setup(bot):
    bot.add_cog(join(bot))