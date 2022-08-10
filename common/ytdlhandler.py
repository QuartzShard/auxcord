import nextcord
import asyncio
import youtube_dl

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'extract_flat': 'in_playlist',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class ytdlSrc(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, playNow = None, toQueue=None, volume=0.5):
        super().__init__(source, volume)
        self.data = data

        if not playNow:
            self.title = data.get('title')
        else:
            self.title = playNow.get('title')
        self.toQueue = toQueue
        self.url = playNow.get('webpage_url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        except youtube_dl.DownloadError as er:
            return None

        q = None
        if 'entries' in data:
            if len(data['entries']) > 1:
                playlistLength = len(data['entries'])
                q = data['entries'][1:playlistLength]
            p = data['entries'][0]
            return {
                'title':p['title'],
                'url':p['url'],
                'toQueue':q
                }
        else:
            p = data
            filename = p['url'] if stream else ytdl.prepare_filename(data)
            return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data, playNow=p, toQueue=q)
           
