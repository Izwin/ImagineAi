import json
from urllib.request import urlopen

def getOpenArtList(query):
    urlstr = "https://openart.ai/api/search?source=dalle2&query=" + query.replace(" ", "%20")
    output = urlopen(urlstr).read()
    j = output.decode('utf-8')

    payload = []
    for row in json.loads(j)["items"]:
        payload.append(row["image_url"])
    return payload