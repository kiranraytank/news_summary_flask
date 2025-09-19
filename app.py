from flask import Flask, render_template, request
from rss_reader import fetch_filtered_articles
from summarizer import summarize_text
from trending import extract_keywords
import nltk
from nltk.corpus import stopwords

app = Flask(__name__)

# Only download once
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')


@app.route('/', methods=['GET', 'POST'])
def index():
    mode = "all"
    selected_keywords = []
    articles = []
    summaries = []
    tags_list = []

    if request.method == 'POST':
        mode = request.form.get('mode', 'all')
        if mode == 'keyword':
            selected_keywords = request.form.getlist('keywords')

    # fetch articles
    if mode == 'all':
        articles = fetch_filtered_articles()
    else:
        articles = fetch_filtered_articles(selected_keywords)

    for article in articles:
        summary = summarize_text(article['summary'])
        tags = extract_keywords(article['summary'])
        summaries.append(summary)
        tags_list.append(tags)

    return render_template(
        'index.html',
        articles=articles,
        summaries=summaries,
        tags_list=tags_list,
        mode=mode,
        selected_keywords=selected_keywords,
        zip=zip
    )


if __name__ == '__main__':
    app.run(debug=True)
