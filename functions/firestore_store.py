"""Firestore data storage for player stats and card kisses"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


class FirestorePlayerStatsStore:
    """Store and retrieve player stats using Cloud Firestore"""

    def __init__(self):
        self.db = firestore.Client()
        self.players_collection = self.db.collection('players')
        self.cards_collection = self.db.collection('cards')

    def save_stats(self, player_tag: str, player_data: Dict) -> Dict:
        """Save player stats with timestamp"""
        # Extract comprehensive stats for historical tracking
        stats = {
            'timestamp': firestore.SERVER_TIMESTAMP,
            'player_tag': player_tag,
            'name': player_data.get('name'),
            'exp_level': player_data.get('expLevel'),

            # Trophy stats
            'trophies': player_data.get('trophies'),
            'best_trophies': player_data.get('bestTrophies'),

            # Battle stats
            'wins': player_data.get('wins'),
            'losses': player_data.get('losses'),
            'three_crown_wins': player_data.get('threeCrownWins', 0),
            'battle_count': player_data.get('battleCount', 0),

            # Clan stats
            'clan_name': player_data.get('clan', {}).get('name'),
            'clan_tag': player_data.get('clan', {}).get('tag'),
            'clan_role': player_data.get('role'),
            'donations': player_data.get('donations', 0),
            'donations_received': player_data.get('donationsReceived', 0),
            'total_donations': player_data.get('totalDonations', 0),

            # Challenge/Tournament stats
            'challenge_cards_won': player_data.get('challengeCardsWon', 0),
            'challenge_max_wins': player_data.get('challengeMaxWins', 0),
            'tournament_cards_won': player_data.get('tournamentCardsWon', 0),
            'tournament_battle_count': player_data.get('tournamentBattleCount', 0),

            # War stats
            'war_day_wins': player_data.get('warDayWins', 0),
            'clan_cards_collected': player_data.get('clanCardsCollected', 0),

            # Card collection stats
            'total_cards': len(player_data.get('cards', [])),
            'star_points': player_data.get('starPoints', 0),
        }

        # Save to Firestore: players/{player_tag}/stats/{timestamp}
        player_doc = self.players_collection.document(player_tag)
        stats_collection = player_doc.collection('stats')

        # Use timestamp as document ID for easy querying
        timestamp_id = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        stats_collection.document(timestamp_id).set(stats)

        return stats

    def get_player_history(self, player_tag: str, limit: Optional[int] = None) -> List[Dict]:
        """Get historical stats for a player"""
        player_doc = self.players_collection.document(player_tag)
        stats_collection = player_doc.collection('stats')

        query = stats_collection.order_by('timestamp', direction=firestore.Query.DESCENDING)

        if limit:
            query = query.limit(limit)

        docs = query.stream()

        history = []
        for doc in docs:
            data = doc.to_dict()
            # Convert Firestore timestamp to ISO string
            if data.get('timestamp'):
                data['timestamp'] = data['timestamp'].isoformat()
            history.append(data)

        return history

    def get_latest_stats(self, player_tag: str) -> Optional[Dict]:
        """Get most recent stats for a player"""
        history = self.get_player_history(player_tag, limit=1)
        return history[0] if history else None

    def get_all_tracked_players(self) -> List[str]:
        """Get list of all tracked player tags"""
        players = self.players_collection.stream()
        return [player.id for player in players]

    def calculate_trends(self, player_tag: str, days: int = 7) -> Optional[Dict]:
        """Calculate stat trends over time"""
        history = self.get_player_history(player_tag, limit=100)  # Get recent history

        if not history or len(history) < 2:
            return None

        # Filter to last N days
        cutoff_date = datetime.now(timezone.utc).timestamp() - (days * 24 * 60 * 60)
        recent = []

        for stat in history:
            if stat.get('timestamp'):
                # Parse ISO timestamp
                from dateutil import parser
                ts = parser.parse(stat['timestamp']).timestamp()
                if ts >= cutoff_date:
                    recent.append(stat)

        if len(recent) < 2:
            return None

        # Calculate changes (most recent vs oldest in period)
        latest = recent[0]
        oldest = recent[-1]

        trends = {
            'trophy_change': int(latest.get('trophies', 0) - oldest.get('trophies', 0)),
            'win_change': int(latest.get('wins', 0) - oldest.get('wins', 0)),
            'loss_change': int(latest.get('losses', 0) - oldest.get('losses', 0)),
            'three_crown_change': int(latest.get('three_crown_wins', 0) - oldest.get('three_crown_wins', 0)),
            'days_tracked': days,
            'data_points': len(recent),
            'win_rate': None
        }

        # Calculate win rate if we have battle data
        total_battles = trends['win_change'] + trends['loss_change']
        if total_battles > 0:
            trends['win_rate'] = round((trends['win_change'] / total_battles) * 100, 1)

        return trends


class FirestoreCardKissTracker:
    """Track card kisses in Firestore"""

    def __init__(self):
        self.db = firestore.Client()
        self.cards_collection = self.db.collection('cards')

    def add_kiss(self, card_name: str) -> int:
        """Add a kiss to a card and return new count"""
        card_doc = self.cards_collection.document(card_name)

        # Use transaction to safely increment
        @firestore.transactional
        def update_in_transaction(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)

            if snapshot.exists:
                current_kisses = snapshot.get('kisses') or 0
                new_kisses = current_kisses + 1
            else:
                new_kisses = 1

            transaction.set(doc_ref, {
                'name': card_name,
                'kisses': new_kisses,
                'updated_at': firestore.SERVER_TIMESTAMP
            }, merge=True)

            return new_kisses

        transaction = self.db.transaction()
        return update_in_transaction(transaction, card_doc)

    def remove_kiss(self, card_name: str) -> int:
        """Remove a kiss from a card and return new count"""
        card_doc = self.cards_collection.document(card_name)

        @firestore.transactional
        def update_in_transaction(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)

            if snapshot.exists:
                current_kisses = snapshot.get('kisses') or 0
                new_kisses = max(0, current_kisses - 1)  # Don't go below 0
            else:
                new_kisses = 0

            transaction.set(doc_ref, {
                'name': card_name,
                'kisses': new_kisses,
                'updated_at': firestore.SERVER_TIMESTAMP
            }, merge=True)

            return new_kisses

        transaction = self.db.transaction()
        return update_in_transaction(transaction, card_doc)

    def get_card_kisses(self, card_name: str) -> int:
        """Get kiss count for a card"""
        card_doc = self.cards_collection.document(card_name).get()

        if card_doc.exists:
            return card_doc.to_dict().get('kisses', 0)
        return 0

    def get_leaderboard(self, limit: int = 50) -> List[tuple]:
        """Get top kissed cards"""
        query = (self.cards_collection
                .where(filter=FieldFilter('kisses', '>', 0))
                .order_by('kisses', direction=firestore.Query.DESCENDING)
                .limit(limit))

        docs = query.stream()

        leaderboard = []
        for doc in docs:
            data = doc.to_dict()
            leaderboard.append((data.get('name'), data.get('kisses', 0)))

        return leaderboard
