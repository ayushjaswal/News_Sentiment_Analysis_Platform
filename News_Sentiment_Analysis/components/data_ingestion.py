import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from News_Sentiment_Analysis.logging.logger import logging
from News_Sentiment_Analysis.exception.exception import NewsSentimentAnalysisException
from datetime import datetime

class DataIngestion:
    def __init__(self):
        self.articles = []
        self.categories = []
        self.title = []

    def get_bbc_articles(self):
        try:
            categories_to_scrape = [
                "https://www.bbc.com/news/world/asia",
                "https://www.bbc.com/business",
                "https://www.bbc.com/news",
                "https://www.bbc.com/innovation",
            ]
            article_links = []

            logging.info("Started Scraping BBC for links")

            for category in categories_to_scrape:
                cat_res = requests.get(category)
                cat_soup = BeautifulSoup(cat_res.content, "html.parser")
                for link in cat_soup.find_all("a", href=True):
                    href = link["href"]
                    if href.startswith("/news/articles/") and href not in article_links:
                        article_links.append(
                            ["https://www.bbc.com" + href, f"{category[20:]}"]
                        )
            urls_to_scrape = article_links
            articles = []
            cats = []
            title = []

            logging.info("Scraping BBC Urls")

            for url in urls_to_scrape:
                response = requests.get(url=url[0])
                soup = BeautifulSoup(response.content, "html.parser")
                text = ""
                body = soup.body
                heading = body.find("h1", class_="sc-518485e5-0 itISwu").get_text(strip=True)
                vals = body.find('article').find_all("p", class_="sc-eb7bd5f6-0 fezwLZ")
                for val in vals:
                    text += val.get_text()
                articles.append(text)
                cats.append(url[1])
                title.append(heading)

            logging.info("BBC Scraping Complete")

            return articles, cats, title
        except Exception as e:
            raise NewsSentimentAnalysisException(e)

    def get_mint_articles(self):
        categories_to_scrape = [
            "https://www.livemint.com/news/india",
            "https://www.livemint.com/news/world",
        ]
        article_links = []
        
        logging.info("Started Scraping Mint for links")
        
        for category in categories_to_scrape:
            cat_res = requests.get(category)
            cat_soup = BeautifulSoup(cat_res.content, "html.parser")
            for link in cat_soup.find_all("a", href=True):
                href = link["href"]
                if href.startswith("/news/") and href not in article_links:
                    article_links.append(
                        ["https://www.livemint.com" + href, f"{category[20:]}"]
                    )
        urls_to_scrape = article_links
        articles = []
        cats = []
        title = []
        try:
            logging.info("Scraping Mint Urls")
            for url in urls_to_scrape:
                response = requests.get(url=url[0])
                soup = BeautifulSoup(response.content, "html.parser")
                text = ""
                body = soup.body
                vals = body.find("div", class_="storyPage_storyContent__m_MYl")
                heading = body.find('h1', id="article-0")
                if vals and heading:
                    vals = vals.find("div", class_="storyParagraph").find_all("p")
                    for val in vals:
                        text += val.get_text()
                    articles.append(text)
                    cats.append(url[1])
                    title.append(heading.get_text())
        except Exception as e:
            print(e)
            print(url)
            raise e

        logging.info("Mint Scraping Complete")
        return articles, cats, title

    def get_ie_articles(self):
        categories_to_scrape = [
            "https://indianexpress.com/section/india/",
            "https://indianexpress.com/section/world/",
        ]
        article_links = []

        logging.info("Started Scraping IE for links")

        for category in categories_to_scrape:
            cat_res = requests.get(category)
            cat_soup = BeautifulSoup(cat_res.content, "html.parser")
            for link in cat_soup.find_all("a", href=True):
                href = link["href"]
                if href.__contains__("/article/") and href not in article_links:
                    article_links.append(
                        [href, f"{category[26:]}"]
                    )
        urls_to_scrape = article_links
        articles = []
        cats = []
        title = []
        logging.info("Scraping IE Urls")
        try:
            for url in urls_to_scrape:
                response = requests.get(url=url[0])
                soup = BeautifulSoup(response.content, "html.parser")
                text = ""
                body = soup.body
                vals = body.find("div", class_="story_details")
                heading = body.find('h1', id="main-heading-article")
                if vals and heading:
                    vals = vals.find_all('p')
                    for val in vals:
                        text += val.get_text()
                    # print(len(text))
                    articles.append(text)
                    cats.append(url[1])
                    title.append(heading.get_text())
            logging.info("IE Scraping Complete")
        except Exception as e:
            print(e)
            print(url)
            raise e

        return articles, cats, title
    
    def get_it_articles(self):
        categories_to_scrape = [
            "https://www.indiatoday.in/world/",
            "https://www.indiatoday.in/india/",
        ]

        article_links = []
        
        logging.info("Started Scraping IT for links")

        for category in categories_to_scrape:
            cat_res = requests.get(category)
            cat_soup = BeautifulSoup(cat_res.content, "html.parser")
            for link in cat_soup.find_all("a", href=True):
                href = link["href"]
                if href.startswith("/world/") or href.startswith("/india/") and href not in article_links:
                    article_links.append(
                        ["https://www.indiatoday.in" + href, f"{category[31:]}"]
                    )
        urls_to_scrape = article_links
        articles = []
        cats = []
        title = []

        logging.info("Scraping IT Urls")

        try:
            for url in urls_to_scrape:
                response = requests.get(url=url[0])
                soup = BeautifulSoup(response.content, "html.parser")
                text = ""
                body = soup.body
                vals = body.find("div", class_="jsx-ace90f4eca22afc7 Story_description__fq_4S description paywall")
                heading = body.find('h1', class_="jsx-ace90f4eca22afc7 Story_strytitle__MYXmR")
                if vals and heading:
                    vals = vals.find_all('p')
                    for val in vals:
                        text += val.get_text()
                    # print(len(text))
                    articles.append(text)
                    cats.append(url[1])
                    title.append(heading.get_text())
            logging.info("IT Scraping Complete")
        except Exception as e:
            print(e)
            print(url)
            raise e

        return articles, cats, title

    def make_data_object(self):
        articles_bbc, category_bbc, title_bbc = self.get_bbc_articles()
        article_mint, category_mint, title_mint = self.get_mint_articles()
        article_ie, category_ie, title_ie = self.get_ie_articles()
        article_it, category_it, title_it = self.get_it_articles()
        self.articles += articles_bbc + article_mint + article_ie + article_it
        self.categories += category_bbc + category_mint + category_ie + category_it
        self.title += title_bbc + title_mint + title_ie + title_it

    def save_data_csv(self):
        data = pd.DataFrame({"title": self.title, "article": self.articles, "category": self.categories})
        data = data.drop_duplicates()
        file_path = f"./News_Sentiment_Analysis/data/articles_{datetime.today().strftime('%Y-%m-%d_%H-%M')}.csv"
        data.to_csv(file_path, index=False)
        logging.info(f"Saved Data to {file_path}")


if __name__ == "__main__":
    obj = DataIngestion()
    obj.make_data_object()
    obj.save_data_csv()
