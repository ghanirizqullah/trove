import yt_dlp
import os

URLS = ['https://www.youtube.com/watch?v=Ej8RhiSv2-4']

def download_audio(url, output_path = 'downloads'):
    os.makedirs(output_path, exist_ok=True)
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s')
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # pyright: ignore[reportArgumentType]
        ydl.download(url)

def main():
    download_audio(URLS)

if __name__ == '__main__':
    main()
 