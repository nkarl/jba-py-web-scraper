"""Module: Web Scraper"""
import requests
from bs4 import BeautifulSoup
import re
import engine.core as core

if __name__ == "__main__":
    fromEntry: str = "https://www.nature.com/nature/articles"
    # core.scrape_articles(fromEntry)
    scraper = core.NatureScraper()
    article_links = scraper.get_article_links_of_type(fromEntry)
