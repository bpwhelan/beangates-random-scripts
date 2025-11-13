
# Script to count characters in a specified field for Anki cards matching a query using AnkiConnect
# Requires: Anki running with AnkiConnect add-on

import requests

# --- USER CONFIGURATION ---
ANKICONNECT_URL = "http://localhost:8765"
QUERY = "SentenceAudio: tag:Tool::GameSentenceMiner"  # Example: all cards in 'Default' deck
FIELD_NAME = "Sentence"    # Field to count characters in
# -------------------------

def invoke(action, **params):
	return requests.post(ANKICONNECT_URL, json={
		"action": action,
		"version": 6,
		"params": params
	}).json()

def main():
	# Find card IDs matching the query
	resp = invoke("findCards", query=QUERY)
	card_ids = resp.get("result", [])
	if not card_ids:
		print("No cards found for query.")
		return
	# Get card info
	info = invoke("cardsInfo", cards=card_ids)
	cards = info.get("result", [])
	total_chars = 0
	for card in cards:
		fields = card.get("fields", {})
		field_value = fields.get(FIELD_NAME, {}).get("value", "")
		char_count = len(str(field_value))
		print(f"Card ID {card['cardId']}: {char_count} characters in '{FIELD_NAME}'")
		total_chars += char_count
	print(f"\nTotal characters in field '{FIELD_NAME}': {total_chars}")

if __name__ == "__main__":
	main()
