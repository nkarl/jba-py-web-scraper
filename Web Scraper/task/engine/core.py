import bs4.element
import requests
import functools
import string
import re

from bs4 import BeautifulSoup
from typing import Final

# default language setting & the host to be scraped
DEFAULT_LANG: Final = {'Accept-Language': 'en-US,en;q=0.5'}
NATURE_SOURCE: Final = "https://www.nature.com"
PUNCTUATION: Final = string.punctuation


def request_response(url: str) -> requests.models.Response:
    r = requests.get(url, headers=DEFAULT_LANG)
    if "20" not in str(r.status_code):
        print(f"The URL returned {r.status_code}")
    return r


# def collect_links(r: requests.models.Response) -> [str]:
#     soup = BeautifulSoup(r.content, "html.parser")
#     links = soup.find_all('article', href=re.compile("/articles/"), itemprop=re.compile("url"))
#     articles = [NATURE_SOURCE + lnk.attrs['href'] for lnk in links]
#     return articles


def collect_articles(r: requests.models.Response) -> [str]:
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("article")
    # links = [(item.find("a").text, item.find("a")["href"]) for item in articles if is_article(item)]
    links = []
    for item in articles:
        if is_article(item):
            a_tag = item.find("a")
            links += [(a_tag.text, a_tag["href"])]
    return links


def is_article(article: bs4.element.Tag) -> bool:
    article_spans = [item.get("data-test", False) for item in article.find_all("span")]
    return "article.type" in article_spans


# def transform_title(content: bytes) -> str:
#     soup = BeautifulSoup(content, "html.parser")
#     title = soup.find("title").text
#     delim = ['|', ':']
#     for d in delim:
#         if d in title:
#             title = '_'.join(title.split(d)[0].split(' '))
#     return title[0:-1] + '.txt'


def scrape_articles(entry: str):
    entry_r = request_response(entry)
    titles, links = collect_articles(entry_r)
    write_articles(links)


def write_articles(links: [str]):
    for link in links:
        content = request_response(link).content
        filename = transform_title(content)
        with open(filename, "wb", encoding="utf-8") as file:
            file.write(content)
