import re

from .util import text_without_children

patterns = (
    "table.infobox.vcard > tbody > tr",
)

def parse_born(born, response):
    parts = re.split("\n+", born)

    if len(parts) == 3:
        response["names"].append(parts[0])
        parts = parts[1:]

    if len(parts) == 2:
        response["birthplace"] = parts[1]

    response["birth_date_raw"] = parts[0]

def scrape_bio(d, items):
    response = {}

    names = [text_without_children(i) for i in d.items("td.nickname > div > ul > li")]

    response["names"] = names

    for row in items:
        elts = row.children()

        header = elts("th")
        data = elts("td")

        if header.text() == "Born":
            parse_born(data.text(), response)

    return response
