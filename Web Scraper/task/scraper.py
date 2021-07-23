"""Module: Web Scraper"""
import requests
from bs4 import BeautifulSoup
import re
import functools

# default language setting
DEFAULT_LANG = {'Accept-Language': 'en-US,en;q=0.5'}
NATURE_SOURCE = "https://www.nature.com"


def grabLinks(url: str):
    # default language settings for requests

    # if "title" not in url:
    #     print("Invalid movie page!")
    # else:
    try:
        r = requests.get(url, headers=DEFAULT_LANG)   # make request
        if "20" not in str(r.status_code):
            raise ValueError
            # print(f"The URL returned {r.status_code}")

        # scrape it here:
        soup = BeautifulSoup(r.content, "html.parser")
        links = soup.find_all('a', href=re.compile("/articles/"), itemprop=re.compile("url"))

        articles = []
        for lnk in links:
            articles += [NATURE_SOURCE + lnk.attrs['href']]

        # title = soup.find("title").text.split(' (')[0]
        # description = soup.find("meta", property=re.compile("description")).attrs['content'].split('. ')[2:]
        # description = description.join(". ")
        # description = functools.reduce(lambda a, b: a + '. ' + b, description)
        # print(description)
        # if title and description is not None:
        #     output = {'title': title, 'description': description}
        #     print(output)
    except ValueError:
        print(f"The URL returned {r.status_code}")
    # except TypeError:
    #     print("Invalid movie page!")


def scrapeArticles(links: [str]):
    # TODO: check if output dir exists, if not create it
    # scrape each file
    pass


def writeIt(url: str):
    r = requests.get(url, headers=DEFAULT_LANG)
    try:
        if "20" not in str(r.status_code):
            print(f"The URL returned {r.status_code}")
        else:
            if r.content:
                content = r.content
                with open("source.html", "wb", encoding='utf-8') as outfile:
                    outfile.write(content)
                print("Content saved.")
    except ValueError:
        print(f"The URL returned {r.status_code}")
    pass


if __name__ == "__main__":
    link: str = input()
    scrapeIt(link)
