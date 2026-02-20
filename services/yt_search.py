import requests
import json


def yt_search(search_term):
    search_url = 'https://www.youtube.com/results?search_query='

    valid_url = search_url + "+".join(search_term.split()) + '+%2Bmusic'
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
            if 'runs' in vids['ownerText']:
                output['owner'] = vids['ownerText']['runs'][0]['text']
            else:
                output['owner'] = 'N/A'
            if 'icon' in vids['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']:
                output['type'] = vids['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['icon']['iconType']
            else:
                output['type'] = 'N/A'
            if 'ownerBadges' in vids:
                output['verification'] = vids['ownerBadges'][0]['metadataBadgeRenderer']['style']
            else:
                output['verification'] = 'N/A'
            output['thumbnail'] = vids['thumbnail']['thumbnails'][0]['url']
            output['link'] = "https://www.youtube.com/watch?v=" + vids['videoId']
            output_container.append(output)
    return output_container

