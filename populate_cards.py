#!/usr/bin/env python3
"""Populate cards master database from sample player response"""
import json
from pathlib import Path

# Load sample player response
sample_file = Path('sample_player_response.json')
if not sample_file.exists():
    print("❌ sample_player_response.json not found!")
    exit(1)

with open(sample_file, 'r') as f:
    player_data = json.load(f)

# Extract all cards
cards_dict = {}
if 'cards' in player_data:
    for card in player_data['cards']:
        card_id = str(card.get('id', 0))
        cards_dict[card_id] = {
            'id': card.get('id', 0),
            'name': card.get('name'),
            'icon_url': card.get('iconUrls', {}).get('medium', ''),
            'max_level': card.get('maxLevel', 0),
            'rarity': card.get('rarity', 'common').capitalize(),
            'elixir_cost': card.get('elixirCost', 0)
        }

# Save to cards master file
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

cards_master_file = data_dir / 'cards_master.json'
with open(cards_master_file, 'w') as f:
    json.dump(cards_dict, f, indent=2)

print(f"✅ Successfully populated {len(cards_dict)} cards to {cards_master_file}")
print(f"\n📊 Card rarities:")
rarities = {}
for card in cards_dict.values():
    rarity = card['rarity']
    rarities[rarity] = rarities.get(rarity, 0) + 1

for rarity, count in sorted(rarities.items()):
    print(f"  {rarity}: {count}")
