"""Migrate cards data to Firestore"""

import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'clashing-stats',
})

db = firestore.client()

# Load cards data
with open('functions/cards_master.json', 'r') as f:
    cards_data = json.load(f)

print(f"Found {len(cards_data)} cards to migrate")

# Migrate each card to Firestore
cards_collection = db.collection('cards')

for card_id, card_info in cards_data.items():
    # Initialize with kiss_count = 0
    card_doc = {
        'id': card_info['id'],
        'name': card_info['name'],
        'icon_url': card_info['icon_url'],
        'max_level': card_info['max_level'],
        'rarity': card_info['rarity'],
        'elixir_cost': card_info['elixir_cost'],
        'kiss_count': 0
    }

    # Use card_id as document ID
    cards_collection.document(card_id).set(card_doc)
    print(f"✓ Migrated {card_info['name']}")

print(f"\n✅ Successfully migrated {len(cards_data)} cards to Firestore!")
