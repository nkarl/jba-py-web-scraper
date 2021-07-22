"""Module: Web Scraper"""
import json
import requests


url = input()
r = requests.get(url)
result = r.json()
try:
    print(result['content'])
except KeyError:
    print("invalid quote resource")