import feedparser
from difflib import SequenceMatcher

rss_feeds = [
    "https://www.theverge.com/rss/index.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.hindustantimes.com/feeds/rss/topnews/rssfeed.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
]

def is_match(keyword, text, threshold=0.6):
    """
    Returns True if keyword matches the text
    using substring or similarity
    """
    keyword = keyword.lower()
    text = text.lower()
    # substring match
    if keyword in text or text in keyword:
        return True
    # similarity match
    return SequenceMatcher(None, keyword, text).ratio() >= threshold

def fetch_filtered_articles(keywords=None):
    """
    Fetch articles and filter based on keywords list.
    Each article includes 'matched_keywords' list
    """
    filtered_articles = []

    if keywords:
        keywords = [kw.lower() for kw in keywords]

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.summary if 'summary' in entry else ''
            content = f"{title} {summary}"

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
                    continue  # skip if no match

            filtered_articles.append({
                'title': title,
                'link': entry.link,
                'summary': summary,
                'tags': tags,
                'matched_keywords': matched
            })

    return filtered_articles
