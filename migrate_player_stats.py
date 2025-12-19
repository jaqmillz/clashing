"""Migrate player stats from Parquet to Firestore"""

import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# Initialize Firebase Admin (if not already initialized)
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'clashing-stats',
    })

db = firestore.client()

# Load player stats from Parquet
df = pd.read_parquet('data/player_stats.parquet')

print(f"Found {len(df)} player stat records to migrate")
print(f"Columns: {list(df.columns)}")

# Group by player_tag to migrate
players_migrated = set()
stats_count = 0

for _, row in df.iterrows():
    player_tag = row.get('player_tag', row.get('tag', None))

    if not player_tag:
        print(f"⚠️ Skipping row with no player_tag")
        continue

    # Clean the player tag
    if not player_tag.startswith('#'):
        player_tag = f'#{player_tag}'

    # Create stats document
    timestamp = row.get('timestamp', row.get('date', datetime.now(timezone.utc)))
    if isinstance(timestamp, str):
        timestamp = pd.to_datetime(timestamp)

    # Create timestamp_id for document
    timestamp_id = timestamp.strftime('%Y%m%d_%H%M%S')

    stats_doc = {
        'timestamp': firestore.SERVER_TIMESTAMP,
        'player_tag': player_tag,
        'trophies': int(row.get('trophies', 0)) if pd.notna(row.get('trophies')) else 0,
        'wins': int(row.get('wins', 0)) if pd.notna(row.get('wins')) else 0,
        'losses': int(row.get('losses', 0)) if pd.notna(row.get('losses')) else 0,
        'level': int(row.get('expLevel', row.get('level', 1))) if pd.notna(row.get('expLevel', row.get('level'))) else 1,
    }

    # Add optional fields
    optional_fields = [
        'name', 'clan_name', 'clan_tag', 'arena', 'best_trophies',
        'three_crown_wins', 'challenge_cards_won', 'tournament_cards_won',
        'donations', 'donations_received', 'total_donations', 'war_day_wins',
        'clan_cards_collected'
    ]

    for field in optional_fields:
        if field in row and pd.notna(row[field]):
            value = row[field]
            if isinstance(value, (int, float)):
                stats_doc[field] = int(value)
            else:
                stats_doc[field] = value

    # Save to Firestore
    player_doc = db.collection('players').document(player_tag)
    stats_collection = player_doc.collection('stats')
    stats_collection.document(timestamp_id).set(stats_doc)

    if player_tag not in players_migrated:
        print(f"✓ Migrated player {player_tag}")
        players_migrated.add(player_tag)

    stats_count += 1

print(f"\n✅ Successfully migrated {stats_count} stats records for {len(players_migrated)} players to Firestore!")
