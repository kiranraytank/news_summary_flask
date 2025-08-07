import feedparser

rss_feeds = [
    "https://www.theverge.com/rss/index.xml",                     # 🥇 Best: summary + proper tags
    "https://www.aljazeera.com/xml/rss/all.xml",                 # 🥈 Good summary + sometimes tags
    "https://feeds.bbci.co.uk/news/rss.xml",                     # 🥉 Consistent structure, summary present
    "https://www.hindustantimes.com/feeds/rss/topnews/rssfeed.xml",  # ⚠️ summary available but fewer tags
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", # ⚠️ summary okay, but almost no tags
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms" # ⚠️ summary okay, tags usually missing
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

            # ✅ Extract tags safely
            tags = []
            if 'tags' in entry:
                tags = [tag.term for tag in entry.tags if 'term' in tag]

            filtered_articles.append({
                'title': title,
                'link': entry.link,
                'summary': summary,
                'tags': tags  # include this in the article dictionary
            })

    return filtered_articles


def fetch_filtered_articles_old(keyword=None):
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
