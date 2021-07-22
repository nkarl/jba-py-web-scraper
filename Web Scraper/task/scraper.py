"""Module: Web Scraper"""
import json
import requests


class MyRequest:
    def __init__(self, url: str):
        self.url = url
        self.response = requests.get(url)
        self.raw = self.response.json()

    def content(self):
        try:
            content = self.raw.get('content', None)
            assert content is not None
            print(content)
        except AssertionError:
            print("Invalid quote resource!")


def get_content(url: str):
    r = requests.get(url)
    requested_json = json.loads(r.text)
    try:
        content = requested_json.get('content', None)
        assert content is not None
        print(content)
    except AssertionError:
        print("Invalid quote resource!")


if __name__ == "__main__":
    link = input()
    # myRequest = MyRequest(link)
    # myRequest.content()
    get_content(link)