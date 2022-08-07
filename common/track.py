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

    async def async_init(self, bot, guild):
        self.loop = bot.loop
        self.handler = await ytdlhandler.ytdlSrc.from_url(self.searchterm, loop=self.loop,stream=True)
        if not self.handler:
            self.restricted = True
        self.title = self.handler.title

    async def play(self, player, guild, after):
        if not self.handler:
            self.handler = await ytdlhandler.ytdlSrc.from_url(self.searchterm, loop=self.loop,stream=True)
        try:
            player.voiceclient.play(self.handler,after=lambda e: after(guild))
        except discord.ClientException as er:
            player.addtoqueue(self)
            if er.args[0] == 'Already playing audio.':
                return lib.embed(
                    title = "Track added to queue",
                    description = self.title
                )
        else:
            if player.queue == []:
                player.addtoqueue(self)
            return lib.embed(
                title = "Now playing:",
                description = self.title
            )
