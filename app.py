from flask import Flask, render_template, request
from rss_reader import fetch_filtered_articles
from summarizer import summarize_text
from trending import extract_keywords
import nltk

app = Flask(__name__)
nltk.download('stopwords')

@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = None
    articles = []
    summaries = []
    tags_list = []

    if request.method == 'POST':
        keyword = request.form['keyword'].strip().lower()

    articles = fetch_filtered_articles(keyword)

    for article in articles:
        summary = summarize_text(article['summary'])
        tags = extract_keywords(article['summary'])
        summaries.append(summary)
        tags_list.append(tags)

    # return render_template('index.html', articles=articles, summaries=summaries, tags_list=tags_list, keyword=keyword)
    return render_template(
        'index.html',
        articles=articles,
        summaries=summaries,
        tags_list=tags_list,
        keyword=keyword,
        zip=zip  # 👈 Add this line
    )


if __name__ == '__main__':
    app.run(debug=True)
