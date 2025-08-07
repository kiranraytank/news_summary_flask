from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_text(text, sentence_count=2):
    try:
        # Check if text is empty or too short for summarization
        if not text or len(text.strip()) < 50:
            return "No summary available."

        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentence_count)

        # Convert summary to string
        summarized_text = ' '.join(str(sentence) for sentence in summary)

        # Additional check: If summary still ends up empty
        if not summarized_text.strip():
            return "No summary available."

        return summarized_text

    except Exception as e:
        # Optional: log the error if needed
        print(f"Summarization error: {e}")
        return "No summary available."
