"""Aggregate all unique cards from stored player data"""
import pandas as pd
import os
import json
from pathlib import Path

DATA_DIR = Path('data')
CARDS_MASTER_FILE = DATA_DIR / 'cards_master.json'

def load_cards_master():
    """Load the master cards database"""
    if CARDS_MASTER_FILE.exists():
        with open(CARDS_MASTER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cards_master(cards_dict):
    """Save the master cards database"""
    DATA_DIR.mkdir(exist_ok=True)
    with open(CARDS_MASTER_FILE, 'w') as f:
        json.dump(cards_dict, f, indent=2)

def update_cards_from_player_data():
    """Update master cards list from player data"""
    cards_dict = load_cards_master()
    updated = False

    # Read the player stats parquet file
    stats_file = DATA_DIR / 'player_stats.parquet'
    if not stats_file.exists():
        return cards_dict

    try:
        df = pd.read_parquet(stats_file)

        # Get the most recent entry for any player (they all have the same full card list)
        if len(df) > 0:
            latest = df.iloc[0]

            # Parse cards JSON if it exists
            if 'cards' in latest and pd.notna(latest['cards']):
                try:
                    cards = json.loads(latest['cards'])
                    for card in cards:
                        card_id = str(card.get('id', 0))
                        if card_id not in cards_dict:
                            cards_dict[card_id] = {
                                'id': card.get('id', 0),
                                'name': card.get('name'),
                                'icon_url': card.get('iconUrls', {}).get('medium', ''),
                                'max_level': card.get('maxLevel', 0),
                                'rarity': card.get('rarity', 'common').capitalize(),
                                'elixir_cost': card.get('elixirCost', 0)
                            }
                            updated = True
                except json.JSONDecodeError as e:
                    print(f"Error parsing cards JSON: {e}")
    except Exception as e:
        print(f"Error reading player stats: {e}")

    # Save if we found new cards
    if updated:
        save_cards_master(cards_dict)

    return cards_dict

def get_all_unique_cards():
    """Get all unique cards, updating from player data if needed"""
    # First try to load from master file
    cards_dict = load_cards_master()

    # If empty or doesn't exist, update from player data
    if not cards_dict:
        cards_dict = update_cards_from_player_data()

    # Convert to list sorted by elixir cost, then name
    cards_list = sorted(cards_dict.values(), key=lambda x: (x.get('elixir_cost', 0), x.get('name', '')))
    return cards_list

def get_cards_dataframe():
    """Get all cards as a pandas DataFrame"""
    cards = get_all_unique_cards()
    if not cards:
        return pd.DataFrame(columns=['name', 'icon_url', 'max_level', 'rarity', 'elixir_cost', 'id'])

    df = pd.DataFrame(cards)
    return df
