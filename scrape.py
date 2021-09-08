#!/usr/bin/env python3

import json
import re
import urllib
from bs4 import BeautifulSoup

URL_PATTERN = re.compile("/boardgame[^/]*/([^/]*)/.*")

def _parse_game_id(url):
    match = URL_PATTERN.match(url)
    if not match:
        print("Bad url:", url)
        return

    return URL_PATTERN.match(url).groups()[0]

def dump_game_ids(filename):
    data = {}
    page = 1
    has_next = True

    while has_next:
        print(f"Page: {page}")
        url = f"https://www.boardgamegeek.com/browse/boardgame/page/{page}"
        resp = urllib.request.urlopen(url)
        soup = BeautifulSoup(resp, features="lxml")

        rows = soup.select("#collectionitems #row_")
        items = [r.select_one("td.collection_objectname a") for r in rows]

        # Add { title: game_id } to data
        for item in items:
            title = item.text
            game_id = _parse_game_id(item["href"])

            if game_id:
                data[title] = game_id

        page += 1
        has_next = soup.select_one("a[title='next page']")

    with open(filename, "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    dump_game_ids("game_ids.json")
