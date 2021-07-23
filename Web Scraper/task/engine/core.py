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
    if "20" not in str(r.status_code):
        print(f"The URL returned {r.status_code}")
    return r
    # try:
    #     if "20" not in str(r.status_code):
    #         raise ValueError
    # except ValueError:
    #     print(f"The URL returned {r.status_code}")
    # else:
    #     return r


def collectLinks(r: requests.models.Response) -> [str]:
    soup = BeautifulSoup(r.content, "html.parser")
    links = soup.find_all('a', href=re.compile("/articles/"), itemprop=re.compile("url"))
    articles = [NATURE_SOURCE + lnk.attrs['href'] for lnk in links]
    return articles


def transformTitle(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    title = soup.find("title").text
    delim = ['|', ':']
    for d in delim:
        if d in title:
            title = '_'.join(title.split(d)[0].split(' '))
    return title[0:-1] + '.txt'


def writeArticles(links: [str]):
    for link in links:
        content = getLinkResponse(link).content
        filename = transformTitle(content)
        with open(filename, "wb") as file:
            file.write(content)


def scrapeArticles(entry: str):
    entry_r = getLinkResponse(entry)
    links = collectLinks(entry_r)
    writeArticles(links)
