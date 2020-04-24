from django.http import JsonResponse

from pyquery import PyQuery as pq
import requests

from urllib.parse import quote

def galactus(req, query):
    url = f"https://google.com/search?q={quote(query, safe='')}"
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": ua}

    contents = requests.get(url, headers=headers).text

    return JsonResponse({
        "urls": [i.attr("href") for i in pq(contents).items("div.r > a")]
    })
