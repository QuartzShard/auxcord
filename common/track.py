## Class to handle information about individual tracks
import boilerBot.lib as lib
from common import ytdlhandler
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

    async def play(self, player, guild, after):
        playlistq = False
        footer = None
        if not self.handler:
            self.handler = await ytdlhandler.ytdlSrc.from_url(self.searchterm, loop=self.loop,stream=True)
        if self.handler.toQueue:
            platlistq = True
            player.addtoqueue(self)
            footer = f"Queued {len(self.handler.toQueue)} tracks from playlist"
            for entry in self.handler.toQueue:
                addtrack = Track(entry['webpage_url'])
                await addtrack.async_init(self.loop, guild)
                player.addtoqueue(addtrack)
        try:
            player.voiceclient.play(self.handler,after=lambda e: after(guild))
        except discord.ClientException as er:
            if not playlistq:
                player.addtoqueue(self)
                if er.args[0] == 'Already playing audio.':
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
