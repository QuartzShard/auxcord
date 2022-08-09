## Class to handle information about what the bot is playing in a server
import boilerBot.lib as lib
class Player():
    def __init__(self, guild, ctx):
        self.guild = guild
        self.queue = []
        self.loop = False
        self.voiceclient = None
        self.ctx = ctx
        self.ispaused = False

    def nowPlaying(self):
        return lib.embed(
            title = "Now Playing:",
            description = f"{self.queue[0].title}"
        )
    
    def addtoqueue(self, track):
        self.queue.append(track)

    def nexttrack(self):
        self.queue[0].handler = None
        if self.loop:
            self.queue.append(self.queue.pop(0))
        else:
            self.queue.pop(0)
        if self.queue != []:
            return self.queue[0]
        else:
            return None
    
    async def connect(self,channel):
        self.voiceclient = await channel.connect()
    