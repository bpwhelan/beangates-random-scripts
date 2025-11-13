import requests
import google.genai as genai
from google.genai.types import GenerationConfig
import os
import dotenv


# Get Gemini API key from environment variable
# API_KEY = os.environ.get("GEMINI_API_KEY")
# if not API_KEY:
#     raise RuntimeError("GEMINI_API_KEY environment variable not set.")
API_KEY = dotenv.get_key(dotenv.find_dotenv(), "GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# The question to ask about each card
QUESTION = "Of all these sentences, which one is the most Samurai Jidai, and very cool and interesting?"
SENTENCE_FIELD = "Sentence"
QUERY = "tag:Game::Sekiro"

ANKICONNECT_URL = "http://localhost:8765"

def get_anki_cards(query):
    """
    Fetch cards from Anki using AnkiConnect based on a query (note name or tag).
    Returns a list of card dicts with cardId, note fields, etc.
    """
    # Find card IDs matching the query (e.g., tag or deck)
    payload = {
        "action": "findCards",
        "version": 6,
        "params": {"query": query}
    }
    resp = requests.post(ANKICONNECT_URL, json=payload)
    card_ids = resp.json().get("result", [])
    if not card_ids:
        return []
    # Get card info
    payload = {
        "action": "cardsInfo",
        "version": 6,
        "params": {"cards": card_ids}
    }
    resp = requests.post(ANKICONNECT_URL, json=payload)
    return resp.json().get("result", [])

def main():
    # query = input("Enter your Anki query (e.g., deck:Default or tag:mytag): ")
    cards = get_anki_cards(QUERY)
    if not cards:
        print("No cards found for query.")
        return
    sentences = []
    for card in cards:
        # Use the card's fields for context
        card_fields = card.get('fields', {})
        if SENTENCE_FIELD in card_fields:
            sentences.append(card_fields[SENTENCE_FIELD]['value'])
    card_text = " | ".join([f"{k}: {v['value']}" for k, v in card_fields.items()])
    
    prompt = f"{QUESTION}\n {sentences}"
    response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
    )
    print(f"Card: {card_text}")
    print(f"Response: {response.text}\n")

if __name__ == "__main__":
    main()
