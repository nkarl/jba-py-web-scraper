"""Module: Web Scraper"""
import requests
from bs4 import BeautifulSoup
import re
import functools


def scrapeIt():
    # default language settings for requests
    default_lang = {'Accept-Language': 'en-US,en;q=0.5'}

    url = input()
    if "title" not in url:
        print("Invalid movie page!")
    else:
        try:
            r = requests.get(url, headers=default_lang)   # make request
            soup = BeautifulSoup(r.content, "html.parser")
            title = soup.find("title").text.split(' (')[0]
            description = soup.find("meta", property=re.compile("description")).attrs['content'].split('. ')[2:]
            # description = description.join(". ")
            description = functools.reduce(lambda a, b: a + '. ' + b, description)
            print(description)
            if title and description is not None:
                output = {'title': title, 'description': description}
                print(output)
        except TypeError:
            print("Invalid movie page!")


if __name__ == "__main__":
    scrapeIt()
