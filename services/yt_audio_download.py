import os
import yt_dlp


def yt_audio_download(url, output_path = 'temp_downloads'):
    os.makedirs(output_path, exist_ok=True)

    filepath = ""

    def get_filepath(d):
        nonlocal filepath
        if d['status'] == 'finished':
            filepath = d['filename']

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'progress_hooks': [get_filepath]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # pyright: ignore[reportArgumentType]
        ydl.download([url])

    return filepath