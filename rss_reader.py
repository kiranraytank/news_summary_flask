import feedparser

rss_feeds = [
    "https://www.theverge.com/rss/index.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.hindustantimes.com/feeds/rss/topnews/rssfeed.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
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

            # ✅ Tags handling
            if 'tags' in entry and entry.tags:
                tags = [tag.term for tag in entry.tags if 'term' in tag]
                if not tags:
                    tags = ["No tags available"]
            else:
                tags = ["No tags available"]

            filtered_articles.append({
                'title': title,
                'link': entry.link,
                'summary': summary,
                'tags': tags
            })

    return filtered_articles
