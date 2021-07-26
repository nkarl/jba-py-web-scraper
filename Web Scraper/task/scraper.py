"""Module: Web Scraper"""
import engine.core as core

if __name__ == "__main__":
    fromEntry: str = "https://www.nature.com/nature/articles"
    scraper = core.NatureNewsScraper()
    scraper.write_articles(fromEntry)
