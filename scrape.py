import json
import urllib
from bs4 import BeautifulSoup


def add_urls(filename, new_urls):
    try:
        with open(filename, "r") as f:
            urls = json.load(f)
    except:
        urls = []

    urls += new_urls

    with open(filename, "w") as f:
        json.dump(urls, f, indent=4, separators=(',', ': '))


def get_bg_urls(filename, page=1):
    print("get_bg_urls: page",page)

    url = "https://www.boardgamegeek.com/browse/boardgame/page/{page}".format(page=page)
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, features="lxml")

    rows = soup.select("#collectionitems #row_")

    urls = [r.select_one("td.collection_objectname a")["href"] for r in rows]

    add_urls(filename, urls)

    has_next = soup.select_one("a[title='next page']")
    if has_next != None:
        get_bg_urls(filename, page + 1)
    else:
        print("Done!")


