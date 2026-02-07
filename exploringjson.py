from pprint import pprint
import json

file = 'initialdata.json'

with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)

    results = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
    inititer = 0
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
        inititer += 1
    print(inititer)
    for i in output_container:
        print(i, end='\n\n')