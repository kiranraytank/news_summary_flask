import nltk
from rake_nltk import Rake
from nltk.corpus import stopwords

# Only download once if missing
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')


def extract_keywords(text, max_words=5):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:max_words]
