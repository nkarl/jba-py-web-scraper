"""Module: Web Scraper"""
import requests
from bs4 import BeautifulSoup
import re
import functools


# def scrapeIt():
#     # default language settings for requests
#     default_lang = {'Accept-Language': 'en-US,en;q=0.5'}
#
#     url = input()
#     if "title" not in url:
#         print("Invalid movie page!")
#     else:
#         try:
#             r = requests.get(url, headers=default_lang)   # make request
#             if r.status_code > 200 + 10:
#                 raise ValueError("Invalid status code.")
#             soup = BeautifulSoup(r.content, "html.parser")
#             title = soup.find("title").text.split(' (')[0]
#             description = soup.find("meta", property=re.compile("description")).attrs['content'].split('. ')[2:]
#             # description = description.join(". ")
#             description = functools.reduce(lambda a, b: a + '. ' + b, description)
#             print(description)
#             if title and description is not None:
#                 output = {'title': title, 'description': description}
#                 print(output)
#         except TypeError:
#             print("Invalid movie page!")


DEFAULT_LANG = {'Accept-Language': 'en-US,en;q=0.5'}


def scrapeIt(url: str):
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
