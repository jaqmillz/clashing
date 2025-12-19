"""Track kisses for Clash Royale cards"""
import json
import os
from pathlib import Path

KISS_DATA_FILE = 'card_kisses.json'

def load_kisses():
    """Load kiss data from JSON file"""
    if os.path.exists(KISS_DATA_FILE):
        with open(KISS_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_kisses(kisses):
    """Save kiss data to JSON file"""
    with open(KISS_DATA_FILE, 'w') as f:
        json.dump(kisses, f, indent=2)

def add_kiss(card_name):
    """Add a kiss to a card"""
    kisses = load_kisses()
    if card_name not in kisses:
        kisses[card_name] = 0
    kisses[card_name] += 1
    save_kisses(kisses)
    return kisses[card_name]

def get_leaderboard(limit=None):
    """Get kiss leaderboard sorted by most kisses"""
    kisses = load_kisses()
    sorted_cards = sorted(kisses.items(), key=lambda x: x[1], reverse=True)
    if limit:
        sorted_cards = sorted_cards[:limit]
    return sorted_cards

def get_card_kisses(card_name):
    """Get kiss count for a specific card"""
    kisses = load_kisses()
    return kisses.get(card_name, 0)

def remove_kiss(card_name):
    """Remove a kiss from a card (slap)"""
    kisses = load_kisses()
    if card_name in kisses and kisses[card_name] > 0:
        kisses[card_name] -= 1
        save_kisses(kisses)
    return kisses.get(card_name, 0)
