#!/usr/bin/env python3
"""Clash Royale Stats Tracker Web App"""

import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from cr_api import ClashRoyaleAPI
from data_store import PlayerStatsStore
from roaster import roast_player, get_performance_emoji, get_skill_rating
from card_aggregator import get_all_unique_cards
from kiss_tracker import add_kiss, get_leaderboard, get_card_kisses, remove_kiss

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize services
cr_api = ClashRoyaleAPI()
data_store = PlayerStatsStore()

DEFAULT_PLAYER_TAG = os.getenv('DEFAULT_PLAYER_TAG', '#2PP')

@app.route('/')
def index():
    return render_template('index.html', default_tag=DEFAULT_PLAYER_TAG)

@app.route('/cards')
def cards_page():
    """Cards gallery page with kiss functionality"""
    return render_template('cards.html')

@app.route('/api/player/<player_tag>')
def get_player_stats(player_tag):
    """Get current player stats and update history"""
    # Fetch from API
    result = cr_api.get_player(player_tag)

    if not result['success']:
        return jsonify(result), 400

    player_data = result['data']

    # Save to historical data
    try:
        data_store.save_stats(player_tag, player_data)
    except Exception as e:
        print(f"Error saving stats: {e}")

    # Get trends
    trends = data_store.calculate_trends(player_tag, days=7)

    # Generate roasts
    roasts = roast_player(player_data, trends)
    performance_emoji = get_performance_emoji(player_data, trends)
    skill_rating = get_skill_rating(player_data, trends)

    return jsonify({
        'success': True,
        'player': player_data,
        'trends': trends,
        'roasts': roasts,
        'performance_emoji': performance_emoji,
        'skill_rating': skill_rating
    })

@app.route('/api/player/<player_tag>/history')
def get_player_history(player_tag):
    """Get historical stats for a player"""
    limit = request.args.get('limit', type=int, default=30)

    history_df = data_store.get_player_history(player_tag, limit=limit)

    if history_df.empty:
        return jsonify({
            'success': False,
            'error': 'No historical data found'
        }), 404

    # Convert to list of dicts for JSON
    history = history_df.to_dict('records')

    # Convert timestamps to strings
    for record in history:
        record['timestamp'] = record['timestamp'].isoformat()

    return jsonify({
        'success': True,
        'history': history
    })

@app.route('/api/tracked-players')
def get_tracked_players():
    """Get all tracked player tags"""
    players = data_store.get_all_tracked_players()
    return jsonify({
        'success': True,
        'players': players
    })

@app.route('/api/save-sample/<player_tag>')
def save_sample_response(player_tag):
    """Save a sample API response to file for review"""
    import json
    result = cr_api.get_player(player_tag)

    if result['success']:
        with open('sample_player_response.json', 'w') as f:
            json.dump(result['data'], f, indent=2)
        return jsonify({
            'success': True,
            'message': f'Sample response saved for {result["data"]["name"]}'
        })
    else:
        return jsonify(result), 400

@app.route('/api/cards')
def get_all_cards():
    """Get all unique cards from stored data"""
    cards = get_all_unique_cards()

    # Add kiss counts to each card
    for card in cards:
        card['kisses'] = get_card_kisses(card['name'])

    return jsonify({
        'success': True,
        'cards': cards
    })

@app.route('/api/cards/kiss', methods=['POST'])
def kiss_card():
    """Add a kiss to a card"""
    data = request.get_json()
    card_name = data.get('card_name')

    if not card_name:
        return jsonify({
            'success': False,
            'error': 'card_name is required'
        }), 400

    new_count = add_kiss(card_name)

    return jsonify({
        'success': True,
        'card_name': card_name,
        'kisses': new_count
    })

@app.route('/api/cards/slap', methods=['POST'])
def slap_card():
    """Remove a kiss from a card (slap)"""
    data = request.get_json()
    card_name = data.get('card_name')

    if not card_name:
        return jsonify({
            'success': False,
            'error': 'card_name is required'
        }), 400

    new_count = remove_kiss(card_name)

    return jsonify({
        'success': True,
        'card_name': card_name,
        'kisses': new_count
    })

@app.route('/api/cards/leaderboard')
def get_kiss_leaderboard():
    """Get kiss leaderboard with card images"""
    limit = request.args.get('limit', type=int, default=50)
    leaderboard = get_leaderboard(limit=limit)

    # Get all cards to find icon URLs
    all_cards = get_all_unique_cards()
    card_map = {card['name']: card for card in all_cards}

    # Add card details to leaderboard
    leaderboard_with_images = []
    for card_name, kisses in leaderboard:
        card_info = card_map.get(card_name, {})
        leaderboard_with_images.append({
            'card_name': card_name,
            'kisses': kisses,
            'icon_url': card_info.get('icon_url', ''),
            'rarity': card_info.get('rarity', 'Common')
        })

    return jsonify({
        'success': True,
        'leaderboard': leaderboard_with_images
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("⚔️  Clash Royale Stats Tracker Starting...")
    print("="*60)
    print(f"\n📊 Default Player: {DEFAULT_PLAYER_TAG}")
    print("\n📍 Open your browser to: http://localhost:3000")
    print("\n⌨️  Press CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=3000)
