import json
import random
import os
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
print("Imported") # I wanted to know if my import was complete or I'll get too impatient

def preprocess(text: str) -> str:
    """
    Simple preprocessing pipeline:
        1. Tokenise.
        2. Lower‑case.
        3. Join tokens back into a string with spaces.
    Returns a space‑joined string ready for TF‑IDF vectorisation.
    """
    tokens = nltk.word_tokenize(text.lower())
    return " ".join(tokens)


# ----------------------------------------------------------------------
# Load corpus (intents, patterns, responses)
# ----------------------------------------------------------------------
def load_corpus(corpus_path: str):
    with open(corpus_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    intents = data.get("intents", [])
    patterns = []
    tags = []
    responses = {}

    for intent in intents:
        tag = intent["tag"]
        responses[tag] = intent.get("responses", [])
        for pattern in intent.get("patterns", []):
            patterns.append(preprocess(pattern))
            tags.append(tag)

    default_responses = data.get("default_responses", [])
    return patterns, tags, responses, default_responses

# Path to the JSON corpus – relative to this script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(BASE_DIR, "corpus.json")

PATTERNS, TAGS, RESPONSES, DEFAULT_RESPONSES = load_corpus(CORPUS_PATH)

# ----------------------------------------------------------------------
# TF‑IDF model
# ----------------------------------------------------------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(PATTERNS)

def predict_tag(sentence: str, threshold: float = 0.3):
    """
    Convert the user sentence into a TF‑IDF vector, compute cosine
    similarity against all stored patterns and return the best‑matching
    tag if the similarity exceeds *threshold*.
    """
    processed = preprocess(sentence)
    query_vec = vectorizer.transform([processed])
    similarities = cosine_similarity(query_vec, X).flatten()
    best_idx = similarities.argmax()
    if similarities[best_idx] < threshold:
        return None
    return TAGS[best_idx]

def get_response(tag: str) -> str:
    """
    Randomly select a response from the list associated with *tag*.
    Falls back to default_responses if tag is unknown.
    """
    if not tag or tag not in RESPONSES:
        return random.choice(DEFAULT_RESPONSES) if DEFAULT_RESPONSES else "I'm sorry, I didn't understand that. Could you re‑phrase?"
    return random.choice(RESPONSES[tag])

# ----------------------------------------------------------------------
# Interactive chat loop
# ----------------------------------------------------------------------
def chat():
    print("Customer Support Bot (type 'quit' to exit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit", "bye"}:
            print("Bot: Goodbye! Have a great day.")
            break

        tag = predict_tag(user_input)
        reply = get_response(tag)
        print(f"Bot: {reply}")

if __name__ == "__main__":
    chat()
