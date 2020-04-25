import re

from .util import text_without_children, text_nodes_without_children

def parse_br(text):
    split = re.split("\n+", text)

    ret = {}

    if len(split) == 3:
        ret["name"] = split[0]
        split = split[1:]
    else:
        ret["name"] = None

    if len(split) == 2:
        ret["date_raw"] = split[0]
        ret["place"] = split[1]
    else:
        ret["date_raw"] = split[0]
        ret["place"] = None

    return ret

def scrape_name(td):
    nickname = td.find(".nickname").text()

    if nickname:
        return nickname

    if td.find("br"):
        return parse_br(td.text())["name"]

def scrape_place(td):
    birthplace = td.find(".birthplace, .deathplace").text()

    if birthplace:
        return birthplace

    if td.find("br"):
        return parse_br(td.text())["place"]

def scrape_date(td):
    if td.find("br"):
        return parse_br(td.text())["date_raw"]
    else:
        return text_nodes_without_children(td.text())[0]

def scrape_born(born, response):
    name = scrape_name(born)
    place = scrape_place(born)
    date = scrape_date(born)

    if name:
        response["names"].append(name)

    if place:
        response["birthplace"] = place

    if date:
        response["birth_date_raw"] = date

def scrape_died(died, response):
    place = scrape_place(died)
    date = scrape_date(died)

    if place:
        response["deathplace"] = place

    if date:
        response["death_date_raw"] = date

def scrape_gender(gender, response):
    response["gender"] = text_without_children(gender)

def scrape_nationality(nationality, response):
    response["nationality"] = text_without_children(nationality)

scrapers = {
    "Born": scrape_born,
    "Died": scrape_died,
    "Gender": scrape_gender,
    "Nationality": scrape_nationality
}

name_patterns = [
    "table.infobox.vcard > tbody > tr > th.fn",
    "table.infobox.vcard > tbody > tr > th > div.fn",
    "td.nickname > div > ul > li",
    "aside.portable-infobox > h2.pi-item"
]

patterns = (
    "table.infobox.vcard > tbody > tr",
    "section.pi-item > div.pi-item"
)

def scrape_bio(d, items):
    response = {}

    names = []

    for pattern in name_patterns:
        for item in d.items(pattern):
            names.append(text_without_children(item))

    response["names"] = names

    for row in items:
        elts = row.children()

        header = elts("th, h3").text()

        if header in scrapers:
            scrapers[header](elts("td, div"), response)

    return response
