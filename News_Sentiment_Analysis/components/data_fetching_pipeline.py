import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from News_Sentiment_Analysis.logging.logger import logging
from News_Sentiment_Analysis.exception.exception import NewsSentimentAnalysisException
import os


class NewsScraper:
    def __init__(self):
        self.articles = []
        self.titles = []
        self.categories = []
        self.routes = {"bbc_news": "https://www.bbc.com/news", "india": ""}
        self.link_filter_fn = {
           "bbc_news": self.bbc_link_filter,
           "india": self.india_link_filter,
        }
        self.article_parsers = {
            "bbc_news": self.bbc_article_parser,
            "india": self.india_article_parser
        }

    def scrape_site(self, topic):
        links = []
        logging.info(f"[{topic}] Collecting article links")
        url = self.routes[topic]
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content, "html.parser")
            links = self.link_filter_fn[topic](soup, topic)
        except Exception as e:
            logging.warning(
                f"[{topic}] Failed to scrape category page {url}: {e}"
            )

        logging.info(
            f"[{topic}] Collected {len(links)} links. Scraping articles..."
        )

        for link, category in links[:5]:
            try:
                res = requests.get(link)
                soup = BeautifulSoup(res.content, "html.parser")
                article_text, title = self.article_parsers[topic](soup)
                if article_text and title:
                    self.articles.append(article_text)
                    self.titles.append(title)
                    self.categories.append(category)
            except Exception as e:
                logging.warning(f"[{topic}] Failed to scrape article {link}: {e}")
        return self.create_csv()

    def create_csv(self):
        df = pd.DataFrame(
            {
                "title": self.titles,
                "article": self.articles,
                "category": self.categories,
            }
        ).drop_duplicates()

        os.makedirs(f"../data/new_scraped", exist_ok=True)
        file_path = f"../data/new_scraped/articles_{datetime.today().strftime('%Y-%m-%d_%H-%M')}.csv"
        df.to_csv(file_path, index=False)
        logging.info(f"Saved dataset with {len(df)} records to {file_path}")
        return df

    def bbc_link_filter(self, soup, base_url):
        article_links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/news/articles/") and href not in article_links:
                article_links.append(["https://www.bbc.com" + href, f"{base_url[20:]}"])
        return article_links

    def bbc_article_parser(self, soup):
        text = ""
        body = soup.body
        heading = body.find("h1", class_="sc-737179d2-0 dAzQyd")
        vals = body.find("article").find_all("p", class_="sc-9a00e533-0 hxuGS")
        for val in vals:
            text += val.get_text()
        return text, heading.get_text(strip=True) if heading else None

    def india_link_filter():
        pass
        
    def india_article_parser():
        pass

if __name__ == "__main__":
    try:
        scraper = NewsScraper()
        data = scraper.scrape_site("bbc_news")
        print(data)

    except Exception as e:
        raise NewsSentimentAnalysisException(e)
