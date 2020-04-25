from django.http import JsonResponse

from pyquery import PyQuery as pq
import requests

from urllib.parse import quote

from . import wiki

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

def scrape(url):
    return pq(requests.get(url, headers={"user-agent": UA}).content)

PATTERNS = {
    wiki.patterns: wiki.scrape_bio
}

def galactus(req, query):
    google_url = f"https://google.com/search?q={quote(query, safe='')}&hl=en"

    urls = [i.attr("href") for i in pq(scrape(google_url)).items("div.r > a")]

    response = {}

    for url in urls:
        try:
            d = scrape(url)
        except:
            continue

        for patterns, fun in PATTERNS.items():
            if isinstance(patterns, str):
                patterns = [patterns]

            for pattern in patterns:
                items = d.items(pattern)

                if items:
                    for k, v in fun(d, items).items():
                        if k not in response or len(v) > len(response[k]):
                            response[k] = v

    return JsonResponse(response)
