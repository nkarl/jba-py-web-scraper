import _io

import requests
import functools
import re

from bs4 import BeautifulSoup


# default language setting
DEFAULT_LANG = {'Accept-Language': 'en-US,en;q=0.5'}
NATURE_SOURCE = "https://www.nature.com"


def getLinkResponse(url: str) -> requests.models.Response:
    r = requests.get(url, headers=DEFAULT_LANG)
    try:
        if "20" not in str(r.status_code):
            raise ValueError
    except ValueError:
        print(f"The URL returned {r.status_code}")
    else:
        return r


def collectLinks(r: requests.models.Response) -> [str]:
    soup = BeautifulSoup(r.content, "html.parser")
    links = soup.find_all('a', href=re.compile("/articles/"), itemprop=re.compile("url"))
    articles = [NATURE_SOURCE + lnk.attrs['href'] for lnk in links]
    return articles


def writeContent(content: bytes, out: _io.BufferedWriter):
    out.write(content)


def scrapeURLs(urls: [str]):
    for url in urls:
        r = getLinkResponse(url).content
