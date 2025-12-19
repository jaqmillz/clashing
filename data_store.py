"""Data storage and historical tracking using Parquet"""

import os
import pandas as pd
from datetime import datetime
from pathlib import Path

class PlayerStatsStore:
    """Store and retrieve player stats using Parquet files"""

    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.stats_file = self.data_dir / 'player_stats.parquet'

    def save_stats(self, player_tag, player_data):
        """Save player stats with timestamp - tracking ALL key metrics"""
        # Extract comprehensive stats for historical tracking
        stats = {
            'timestamp': datetime.now(),
            'player_tag': player_tag,
            'name': player_data.get('name'),
            'exp_level': player_data.get('expLevel'),

            # Trophy stats (change frequently)
            'trophies': player_data.get('trophies'),
            'best_trophies': player_data.get('bestTrophies'),

            # Battle stats (change frequently)
            'wins': player_data.get('wins'),
            'losses': player_data.get('losses'),
            'three_crown_wins': player_data.get('threeCrownWins', 0),
            'battle_count': player_data.get('battleCount', 0),

            # Clan stats (change frequently - donations reset)
            'clan_name': player_data.get('clan', {}).get('name', None),
            'clan_tag': player_data.get('clan', {}).get('tag', None),
            'clan_role': player_data.get('role', None),
            'donations': player_data.get('donations', 0),
            'donations_received': player_data.get('donationsReceived', 0),
            'total_donations': player_data.get('totalDonations', 0),

            # Challenge/Tournament stats (change frequently)
            'challenge_cards_won': player_data.get('challengeCardsWon', 0),
            'challenge_max_wins': player_data.get('challengeMaxWins', 0),
            'tournament_cards_won': player_data.get('tournamentCardsWon', 0),
            'tournament_battle_count': player_data.get('tournamentBattleCount', 0),

            # War stats (change frequently)
            'war_day_wins': player_data.get('warDayWins', 0),
            'clan_cards_collected': player_data.get('clanCardsCollected', 0),

            # Card collection stats (changes as cards upgrade)
            'total_cards': len(player_data.get('cards', [])),
            'star_points': player_data.get('starPoints', 0),
        }

        # Create DataFrame
        new_df = pd.DataFrame([stats])

        # Append to existing data or create new file
        if self.stats_file.exists():
            existing_df = pd.read_parquet(self.stats_file)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df

        # Save to Parquet
        combined_df.to_parquet(self.stats_file, index=False, engine='pyarrow')

        return stats

    def get_player_history(self, player_tag, limit=None):
        """Get historical stats for a player"""
        if not self.stats_file.exists():
            return pd.DataFrame()

        df = pd.read_parquet(self.stats_file)
        player_df = df[df['player_tag'] == player_tag].sort_values('timestamp', ascending=False)

        if limit:
            player_df = player_df.head(limit)

        return player_df

    def get_latest_stats(self, player_tag):
        """Get most recent stats for a player"""
        history = self.get_player_history(player_tag, limit=1)
        if history.empty:
            return None
        return history.iloc[0].to_dict()

    def get_all_tracked_players(self):
        """Get list of all tracked player tags"""
        if not self.stats_file.exists():
            return []

        df = pd.read_parquet(self.stats_file)
        return df['player_tag'].unique().tolist()

    def calculate_trends(self, player_tag, days=7):
        """Calculate stat trends over time"""
        history = self.get_player_history(player_tag)

        if history.empty or len(history) < 2:
            return None

        # Filter to last N days
        cutoff_date = datetime.now() - pd.Timedelta(days=days)
        recent = history[history['timestamp'] >= cutoff_date].copy()

        if len(recent) < 2:
            return None

        # Calculate changes
        latest = recent.iloc[0]
        oldest = recent.iloc[-1]

        trends = {
            'trophy_change': int(latest['trophies'] - oldest['trophies']),
            'win_change': int(latest['wins'] - oldest['wins']),
            'loss_change': int(latest['losses'] - oldest['losses']),
            'three_crown_change': int(latest['three_crown_wins'] - oldest['three_crown_wins']),
            'days_tracked': days,
            'data_points': len(recent),
            'win_rate': None
        }

        # Calculate win rate if we have battle data
        total_battles = trends['win_change'] + trends['loss_change']
        if total_battles > 0:
            trends['win_rate'] = round((trends['win_change'] / total_battles) * 100, 1)

        return trends

    def get_stats_dataframe(self, player_tag):
        """Get full stats DataFrame for advanced analysis"""
        return self.get_player_history(player_tag)
