import bs4.element
import requests
import string
from furl import furl

from bs4 import BeautifulSoup
from typing import Final

# default language setting & the host to be scraped
DEFAULT_LANG: Final = {'Accept-Language': 'en-US,en;q=0.5'}
NATURE_SOURCE: Final = "https://www.nature.com"
PUNCTUATION: Final = string.punctuation
IN_CHARS: Final = PUNCTUATION + " "
OUT_CHARS: Final = ''.join(['_' if c == ' ' else ' ' for c in IN_CHARS])


class NatureNewsScraper:
    @staticmethod
    def request_response(url: str) -> requests.models.Response:
        r = requests.get(url, headers=DEFAULT_LANG)
        if "20" not in str(r.status_code):
            print(f"The URL returned {r.status_code}")
        return r

    @staticmethod
    def tag_containing_view_article(tag: bs4.element) -> bool:
        return tag.has_attr("data-track-action") and \
               tag.get("data-track-action", None) == "view article"

    @staticmethod
    def tag_containing_article_type(tag: bs4.element) -> bool:
        return tag.name == "span" and \
               tag.has_attr("data-test") and \
               tag.get("data-test", None) == "article.type"

    def collect_news_links(self, entry) -> [str]:
        url_origin = furl(entry).origin
        r = self.request_response(entry)
        soup = BeautifulSoup(r.content, "html.parser")
        articles = soup.find_all(self.tag_containing_article_type)
        news_articles = list(filter(lambda x: x.text.strip() == "News", articles))
        return [
            furl(url_origin).add(path=x.find_parent("article").find(self.tag_containing_view_article).get("href")).url \
            for x in news_articles
        ]

    @staticmethod
    def tag_containing_article_title(tag) -> bool:
        return tag.name == "h1" and \
               ("article" in tag["class"][0] and "title" in tag["class"][0])

    @staticmethod
    def tag_containing_article_body(tag) -> bool:
        return tag.name == "div" and \
               ("article" in tag.get("class", [""])[0] and "body" in tag.get("class", [""])[0])

    def scrape_title_and_content(self, url) -> (str, str):
        r = self.request_response(url)
        soup = BeautifulSoup(r.content, "html.parser")
        title = soup.find(self.tag_containing_article_title)
        content = soup.find(self.tag_containing_article_body)
        if title and content:
            return title.text.strip(), content.text.strip()
        else:
            return title, content

    def scrape_articles(self, links: [str]) -> [(str, str)]:
        contents = []
        for link in links:
            contents += [(self.scrape_title_and_content(link))]
        return contents

    @staticmethod
    def transform_title(title: str) -> str:
        dictionary = title.maketrans(IN_CHARS, OUT_CHARS)
        return ''.join(title.translate(dictionary).split(' '))

    def write_articles(self, entry: str):
        links = self.collect_news_links(entry)
        contents = self.scrape_articles(links)
        for url in links:
            title, content = self.scrape_title_and_content(url)
            path = self.transform_title(title)
            with open(path + ".txt", "wb") as file:
                file.write(content.encode(encoding="utf-8"))
