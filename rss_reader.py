import feedparser
from difflib import SequenceMatcher
from datetime import datetime, timedelta


rss_feeds = [
    "https://www.theverge.com/rss/index.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.hindustantimes.com/feeds/rss/topnews/rssfeed.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
]

def is_match(keyword, text, threshold=0.6):
    keyword = keyword.lower()
    text = text.lower()
    if keyword in text or text in keyword:
        return True
    return SequenceMatcher(None, keyword, text).ratio() >= threshold

def fetch_filtered_articles(keywords=None, date_filter=None):
    """
    Fetch articles and filter based on keywords list and date filter.
    Each article includes 'matched_keywords' list
    """
    filtered_articles = []
    if keywords:
        keywords = [kw.lower() for kw in keywords]

    now = datetime.now()

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.summary if 'summary' in entry else ''
            content = f"{title} {summary}"

            # published date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            else:
                published = None

            # date filter
            if date_filter and published:
                if date_filter == 'today' and published.date() != now.date():
                    continue
                elif date_filter == '3days' and published < now - timedelta(days=3):
                    continue
                elif date_filter == 'week' and published < now - timedelta(days=7):
                    continue

            # tags
            if 'tags' in entry and entry.tags:
                tags = [tag.term for tag in entry.tags if 'term' in tag]
                if not tags:
                    tags = ["No tags available"]
            else:
                tags = ["No tags available"]

            matched = []
            if keywords:
                for kw in keywords:
                    if is_match(kw, content) or any(is_match(kw, tag) for tag in tags):
                        matched.append(kw)
                if not matched:
                    continue

            filtered_articles.append({
                'title': title,
                'link': entry.link,
                'summary': summary,
                'tags': tags,
                'matched_keywords': matched,
                'published': published
            })

    return filtered_articles
