import re

import bs4.element
import requests
import string
from furl import furl

from bs4 import BeautifulSoup
from typing import Final
from hstest.check_result import CheckResult

# default language setting & the host to be scraped
DEFAULT_LANG: Final = {'Accept-Language': 'en-US,en;q=0.5'}
NATURE_SOURCE: Final = "https://www.nature.com"
PUNCTUATION: Final = string.punctuation
IN_CHARS: Final = PUNCTUATION + " "
OUT_CHARS: Final = ''.join(['_' if c == ' ' else ' ' for c in IN_CHARS])


def request_response(url: str) -> requests.models.Response:
    r = requests.get(url, headers=DEFAULT_LANG)
    if "20" not in str(r.status_code):
        print(f"The URL returned {r.status_code}")
    return r


def collect_articles(r: requests.models.Response) -> [(str, str)]:
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("article")
    # links = [(item.find("a").text, item.find("a")["href"]) for item in articles if is_article(item)]
    links = []
    for item in articles:
        if is_article(item):
            a_tag = item.find("a")
            links += [(a_tag.text, NATURE_SOURCE+ a_tag["href"])]
    return links


def is_article(article: bs4.element.Tag) -> bool:
    article_spans = [item.get("data-test", False) for item in article.find_all("span")]
    return "article.type" in article_spans


def transform_title(title: str) -> str:
    dictionary = title.maketrans(IN_CHARS, OUT_CHARS)
    return ''.join(title.translate(dictionary).split(' '))


def scrape_articles(entry: str):
    # entry_r = request_response(entry)
    # links = collect_articles(entry_r)
    # articles = get_articles(links)
    # for path, body in articles:
    #     with open(path, "wb") as file:
    #         file.write(body.encode("utf-8"))
    scraper = NatureScraper()
    contents = scraper.get_article_title_and_content(entry)
    return contents



def is_body(soup):
    return soup.find("div", class_=re.compile("article-body")) is not None
    # return body.contents if body is not None else None


def get_articles(links: [(str, str)]):
    articles = []
    for title, link in links:
    # for i in range(9):  # hardcoded to 4 articles
    #     title, link = links[i]
        path = transform_title(title) + ".txt"
        content = request_response(link).content
        soup = BeautifulSoup(content, "html.parser")
        if is_body(soup):
            articles += [(path, soup.find("div", class_=re.compile("article-body")))]
    return articles


class NatureScraper:
    def tag_leading_to_view_article(self, tag):
        return tag.has_attr("data-track-action") and tag["data-track-action"] == "view article"

    def tag_containing_atricle_type(self, tag):
        return tag.name == "span" and tag.has_attr("data-test") and tag.get("data-test", None) == "article.type"

    def tag_containing_article_title(self, tag):
        return tag.name == "h1" and ("article" in tag["class"][0] and "title" in tag["class"][0])

    def tag_containing_article_body(self, tag):
        return tag.name == "div" and ("article" in tag.get("class", [""])[0] and "body" in tag.get("class", [""])[0])

    def get_article_links_of_type(self, url, article_type="News"):
        origin_url = furl(url)
        try:
            articles_resp = requests.get(url)
        except Exception:
            return CheckResult.wrong("An error occurred when tests tried to connect to the Internet page.\n"
                                     "Please, try again.")
        soup = BeautifulSoup(articles_resp.text, "html.parser")
        articles = soup.find_all(self.tag_containing_atricle_type)
        articles = list(filter(lambda x: x.text.strip() == article_type, articles))
        return [
            furl(origin_url).add(path=x.find_parent("article").find(self.tag_leading_to_view_article).get("href")).url \
            for x in articles]

    def get_article_title_and_content(self, url):
        try:
            article = requests.get(url)
        except Exception:
            return CheckResult.wrong("An error occurred when tests tried to connect to the Internet page.\n"
                                     "Please, try again.")
        soup = BeautifulSoup(article.text, "html.parser")
        title = soup.find(self.tag_containing_article_title)
        content = soup.find(self.tag_containing_article_body)
        if title and content:
            return title.text.strip(), content.text.strip()
        else:
            return title, content
