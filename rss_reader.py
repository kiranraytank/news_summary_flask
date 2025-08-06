import feedparser

rss_feeds = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://www.theverge.com/rss/index.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.hindustantimes.com/feeds/rss/topnews/rssfeed.xml",
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
]

def fetch_filtered_articles(keyword=None):
    filtered_articles = []

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.summary if 'summary' in entry else ''
            content = f"{title} {summary}"

            if keyword and keyword.lower() not in content.lower():
                continue

            filtered_articles.append({
                'title': title,
                'link': entry.link,
                'summary': summary
            })

    return filtered_articles
