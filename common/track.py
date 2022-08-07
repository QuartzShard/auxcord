## Class to handle information about individual tracks
import boilerBot.lib as lib
from common import ytdlhandler
import asyncio
import discord
class Track():
    def __init__(self, searchterm):
        self.handler = None
        self.title = None
        self.restricted = False
        self.searchterm = searchterm
        self.loop = None

    async def async_init(self, loop, guild):
        self.loop = loop
        self.handler = await ytdlhandler.ytdlSrc.from_url(self.searchterm, loop=self.loop,stream=True)
        if not self.handler:
            self.restricted = True
            return
        self.title = self.handler.title
        self.searchterm = self.handler.url
        return

    async def play(self, bot, ctx, player, guild, after):
        guildVars = lib.retrieve(guild.id, bot)
        playlistq = False
        footer = None
        if not self.handler:
            self.handler = await ytdlhandler.ytdlSrc.from_url(self.searchterm, loop=self.loop,stream=True)
        try:
            player.voiceclient.play(self.handler,after=lambda e: after(guild))
        except discord.ClientException as er:
            if er.args[0] == 'Already playing audio.':
                playlistq, footer = await self.handlePlaylist(bot, ctx, player, guild, guildVars)
                if not playlistq:
                    player.addtoqueue(self)
                if footer:
                    return lib.embed(
                        title = f"{len(self.handler.toQueue) + 1} tracks added to queue",                           
                    )
                else:
                    return lib.embed(
                        title = "Track added to queue",
                        description = self.title
                    )
        else:
            playlistq, footer = await self.handlePlaylist(bot, ctx, player, guild, guildVars)
            if player.queue == []:
                player.addtoqueue(self)
            if footer:
                return lib.embed(
                    title = "Now playing:",
                    description = self.title,
                    footer = footer
                )
            else:
                return lib.embed(
                    title = "Now playing:",
                    description = self.title,
                )

        
    async def handlePlaylist(self, bot, ctx, player, guild, guildVars):
        try:
            if self.handler.toQueue:
                guildVars["previous"] = await lib.send(ctx,lib.embed(
                    title = "Queueing a playlist",
                    description = "This can take considerable time, especially for larger playlists. Please be patient!",
                    footer = f"Queueing {len(self.handler.toQueue)+1} tracks..."
                ), guildVars["previous"])
                lib.set(guild.id,bot,guildVars)
                player.addtoqueue(self)
                footer = f"Queued {len(self.handler.toQueue)} tracks from playlist"
                for entry in self.handler.toQueue:
                    addtrack = Track(entry['webpage_url'])
                    await addtrack.async_init(self.loop, guild)
                    player.addtoqueue(addtrack)
                    await asyncio.sleep(1)
                return True, footer
            else:
                return False, None
        except AttributeError:
            return False, None