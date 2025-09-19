from math import ceil
from flask import Flask, render_template, request
from rss_reader import fetch_filtered_articles
from summarizer import summarize_text
from trending import extract_keywords
import nltk
from nltk.corpus import stopwords
import re
from markupsafe import Markup
from datetime import datetime, timedelta

app = Flask(__name__)

# Only download once
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

def highlight_keywords(text, keywords):
    if not text or not keywords:
        return text

    def replacer(match):
        return f'<span class="matched">{match.group(0)}</span>'

    pattern = r'(' + '|'.join(re.escape(kw) for kw in keywords) + r')'
    highlighted_text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
    return Markup(highlighted_text)


@app.route('/', methods=['GET', 'POST'])
def index():
    page = int(request.args.get('page', 1))
    per_page = 8

    if request.method == 'POST':
        mode = request.form.get("mode", "all")
        selected_keywords = request.form.getlist("keywords")
        date_filter = request.form.get("date_filter", "all")
    else:
        mode = request.args.get("mode", "all")
        selected_keywords = request.args.getlist("keywords")
        date_filter = request.args.get("date_filter", "all")

    # fetch + filter your articles here using mode and selected_keywords
    if mode == 'all':
        all_articles = fetch_filtered_articles(date_filter=date_filter)
    else:
        all_articles = fetch_filtered_articles(selected_keywords, date_filter=date_filter)

    total_articles = len(all_articles)
    total_pages = ceil(total_articles / per_page)

    # paginate articles
    start = (page - 1) * per_page
    end = start + per_page
    articles = all_articles[start:end]

    summaries = []
    tags_list = []
    for article in articles:
        summary_text = article['summary']
        summary_highlighted = highlight_keywords(summary_text, article['matched_keywords'])
        summaries.append(summary_highlighted)
        tags = extract_keywords(article['summary'])
        tags_list.append(tags)

    return render_template(
        'index.html',
        articles=articles,
        summaries=summaries,
        tags_list=tags_list,
        mode=mode,
        selected_keywords=selected_keywords,
        date_filter=date_filter,
        zip=zip,
        page=page,
        total_pages=total_pages
    )


if __name__ == '__main__':
    app.run(debug=True)
