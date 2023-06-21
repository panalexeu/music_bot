# discord bot token
TOKEN = 'MTEyMDM1NTQ0MzAzNDgyMDY0OA.Gr1EV_.9LHuN2ZE_GCPbd1c_Z-uTL2UlwF4BYN7V-fDvM'

YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_PATH = 'ffmpeg/ffmpeg-2023-06-19-git-1617d1a752-full_build/bin/ffmpeg.exe'

FFMPEG_OPTIONS = {
    'options': '-vn'
}

LOGO_URL = 'https://upload.wikimedia.org/wikipedia/en/0/05/Mug_root_beer_logo.png'