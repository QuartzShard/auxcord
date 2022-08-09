## Class to handle information about individual tracks
import boilerBot.lib as lib
from common import ytdlhandler
import asyncio
import discord
class Track():
    def __init__(self, searchterm,title=None):
        self.handler = None
        self.title = title
        self.restricted = False
        self.searchterm = searchterm
        self.loop = None

    async def async_init(self, loop, guild):
        self.loop = loop
        self.handler = await ytdlhandler.ytdlSrc.from_url(self.searchterm, loop=self.loop,stream=True)
        if not self.handler:
            self.restricted = True
            return
        if type(self.handler) == dict:
            self.title = self.handler['title']
            self.searchterm = self.handler['url']
            self.toQueue = self.handler['toQueue']
            self.handler = await ytdlhandler.ytdlSrc.from_url(self.searchterm, loop=self.loop,stream=True)
        else:
            self.title = self.handler.title
            self.searchterm = self.handler.url
            self.toQueue = self.handler.toQueue
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
                playlistq, footer = await self.handlePlaylist(player)
                if not playlistq:
                    player.addtoqueue(self)
                if footer:
                    return lib.embed(
                        title = f"{len(self.toQueue) + 1} tracks added to queue",                           
                    )
                else:
                    return lib.embed(
                        title = "Track added to queue",
                        description = self.title
                    )
        except:
            playlistq, footer = await self.handlePlaylist(player)
            if not playlistq:
                player.addtoqueue(self)
            return lib.embed(
                title="Something went wrong playing that track",
                colour=lib.errorColour
            )
            
        else:
            playlistq, footer = await self.handlePlaylist(player)
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

        
    async def handlePlaylist(self, player):
        try:
            if self.toQueue:
                player.addtoqueue(self)
                footer = f"Queued {len(self.toQueue)} tracks from playlist"
                for entry in self.toQueue:
                    addtrack = Track(entry['url'], entry['title'])
                    player.addtoqueue(addtrack)
                return True, footer
            else:
                return False, None
        except AttributeError:
            return False, None