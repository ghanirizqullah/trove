import os
import yt_dlp
from io import BytesIO
import tempfile


def yt_audio_download(url):
    # Create a temporary directory that will be cleaned up automatically
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_file_path = None
        
        def get_filepath(d):
            nonlocal audio_file_path
            if d['status'] == 'finished':
                audio_file_path = d['filename']
        
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [get_filepath]
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
            ydl.download([url])
        
        # Read the downloaded file into memory
        if audio_file_path and os.path.exists(audio_file_path):
            with open(audio_file_path, 'rb') as f:
                file_data = BytesIO(f.read())
            
            # Extract filename for the browser
            filename = os.path.basename(audio_file_path)
            
            # Return both the in-memory file and filename
            return file_data, filename
        
    return None, None