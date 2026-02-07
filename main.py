import yt_dlp
import os
import requests
import json
import pprint

# URLS = ['https://www.youtube.com/watch?v=Ej8RhiSv2-4']
URLS = ['https://music.youtube.com/watch?v=Vj2VHNvkBPA']


def download_audio(url, output_path = 'downloads'):
    os.makedirs(output_path, exist_ok=True)
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s')
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # pyright: ignore[reportArgumentType]
        ydl.download(url)

def yt_search(search_term):
    search_url = 'https://www.youtube.com/results?search_query='

    valid_url = search_url + "+".join(search_term.split())
    response = requests.get(valid_url).text

    start = (
        response.index("ytInitialData")
        + len("ytInitialData")
        + 3
    )
    end = response.index("};", start) + 1
    json_str = response[start:end]
    data = json.loads(json_str)

    results = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
    output_container = []
    for items in results:
        if "videoRenderer" in items:
            output = {}
            vids = items.get("videoRenderer", {})
            output['title'] = vids['title']['runs'][0]['text']
            output['owner'] = vids['ownerText']['runs'][0]['text']
            if 'ownerBadges' in vids:
                output['verification'] = vids['ownerBadges'][0]['metadataBadgeRenderer']['style']
            else:
                output['verification'] = 'N/A'
            output['link'] = "https://www.youtube.com/watch?v=" + vids['videoId']
            output_container.append(output)
    for i in output_container:
        print(i, end='\n\n')



def main():
    search = input()
    yt_search(search)

if __name__ == '__main__':
    main()
 