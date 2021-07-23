import _io

import requests
import functools
import re
import os.path

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


def getArticleTitle(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    title = getArticleTitle(soup.find("title").text)
    return transformTitle(title)


def transformTitle(title: str):
    return '_'.join(title.split(' |')[0].split(' '))


def scrapeURLs(links: [str]):
    for link in links:
        content = getLinkResponse(link).content
        filename = getArticleTitle(content)
        filename += ".txt"
        with open(filename, "wb") as file:
            file.write(content)
    pass
