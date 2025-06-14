# -*- coding: utf-8 -*-
"""emotion_classifier/preprocess.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17lAaDskGGC6UrQVfeAp7vm8pjCphZHN2
"""

# emotion_classifier/preprocess.py
import re
import nltk
from nltk.stem import WordNetLemmatizer
# NLTK resources will be checked/downloaded by model_loader.py at first run if needed.

# Global lemmatizer instance (can be initialized in a function if preferred)
# Ensure NLTK data is downloaded before this module is heavily used,
# or initialize lazily. For CLI, it's often fine to initialize globally.
try:
    lemmatizer = WordNetLemmatizer()
    # Test lemmatization to trigger download if not present and not handled elsewhere
    lemmatizer.lemmatize("runs")
except LookupError:
    print("NLTK WordNet resource not found. Please ensure it's downloaded.")
    # In a CLI, you might want to trigger download here or guide the user.
    # For simplicity in this example, we assume it's handled by model_loader or pre-downloaded.
    pass


def preprocess_text_for_cli(text, remove_stopwords=False, lemmatize=True):
    """
    Cleans text data for inference: lowercase, remove URLs, mentions, hashtags symbols, punctuation.
    Optionally removes stopwords and applies lemmatization.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "<URL>", text, flags=re.MULTILINE)
    text = re.sub(r"\@\w+", "<USER>", text)
    text = re.sub(r"\#\w+", lambda m: m.group(0).replace("#", "<HASHTAG>"), text) # Keep hashtag text
    text = re.sub(r"[^a-z0-9\s<>!?.,']", "", text) # Keep some punctuation

    text_tokens = text.split()

    # Stopword removal is optional and might depend on your final model's training
    if remove_stopwords:
        try:
            # Ensure stopwords are available
            stop_words = set(nltk.corpus.stopwords.words('english'))
            text_tokens = [word for word in text_tokens if word not in stop_words]
        except LookupError:
            print("NLTK stopwords resource not found. Skipping stopword removal.")


    if lemmatize:
        try:
            # Lemmatizer should be initialized globally or passed in
            text_tokens = [lemmatizer.lemmatize(word) for word in text_tokens]
        except Exception as e: # Catch if lemmatizer failed (e.g. WordNet not found)
            print(f"Lemmatization failed: {e}. Skipping lemmatization.")


    return " ".join(text_tokens)