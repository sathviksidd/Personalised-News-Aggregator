import requests
from bs4 import BeautifulSoup
from google.cloud import language_v1
import os
from config import GCLOUD_CREDENTIALS_PATH

# Authenticate Google Cloud NLP API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCLOUD_CREDENTIALS_PATH

# Initialize Google Cloud NLP client
client = language_v1.LanguageServiceClient()

def fetch_news(url):
    """Fetch news articles from a given URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')  # Use 'xml' parser
    articles = []
    for item in soup.find_all('item'):
        title = item.find('title').text
        link = item.find('link').text
        articles.append({'title': title, 'link': link})
    return articles

def extract_keywords(text):
    """Extract keywords from text using Google Cloud NLP API."""
    try:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en")  # Specify language as English
        response = client.analyze_entities(document=document)
        keywords = [entity.name for entity in response.entities]
        return keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

def get_news_sources():
    """Return a list of news sources relevant to India."""
    sources = [
        'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
        'https://www.hindustantimes.com/rss/topnews/rssfeed.xml',
        'https://indianexpress.com/feed/',
        'https://feeds.feedburner.com/ndtvnews-top-stories',
        'https://www.thehindu.com/feeder/default.rss',
        'https://www.dnaindia.com/feeds/latest-news.xml',
        'https://www.news18.com/rss/world.xml',
        'https://www.indiatoday.in/rss/home',
        'https://economictimes.indiatimes.com/rssfeedsdefault.cms',
        'https://www.financialexpress.com/feed/',
        'https://www.livemint.com/rss/news',
        'https://www.deccanchronicle.com/feed',
        'https://www.business-standard.com/rss/home_page_top_stories.rss',
        'https://www.thequint.com/rss',
        'https://www.tribuneindia.com/rss/feed',
    ]
    return sources

def scrape_all_sources():
    """Scrape all news sources and return a list of articles with keywords."""
    news_sources = get_news_sources()
    all_articles = []
    for source in news_sources:
        try:
            articles = fetch_news(source)
            for article in articles:
                keywords = extract_keywords(article['title'])
                article['keywords'] = keywords
                all_articles.append(article)
        except Exception as e:
            print(f"Error fetching or processing articles from {source}: {e}")
    return all_articles
