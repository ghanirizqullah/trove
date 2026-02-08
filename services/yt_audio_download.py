import os
import yt_dlp

def yt_audio_download(url, output_path = 'downloads'):
    os.makedirs(output_path, exist_ok=True)
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s')
        
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # pyright: ignore[reportArgumentType]
        ydl.download(url)