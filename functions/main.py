"""Cloud Functions for Clash Royale Stats Tracker"""

import os
import json
from firebase_functions import https_fn, options
from firebase_admin import initialize_app
from cr_api import ClashRoyaleAPI
from firestore_store import FirestorePlayerStatsStore, FirestoreCardKissTracker
from roaster import roast_player, get_performance_emoji, get_skill_rating
from card_aggregator import get_all_unique_cards

# Initialize Firebase Admin
initialize_app()

# Initialize services
# API key will be set via environment variable/secret
cr_api = ClashRoyaleAPI()
data_store = FirestorePlayerStatsStore()
kiss_tracker = FirestoreCardKissTracker()

# CORS configuration for all functions
cors_options = options.CorsOptions(
    cors_origins="*",
    cors_methods=["get", "post", "options"],
)


@https_fn.on_request(cors=cors_options)
def get_player_stats(req: https_fn.Request) -> https_fn.Response:
    """Get current player stats and update history

    Route: /api/player/<player_tag>
    Method: GET
    """
    # Extract player_tag from path: /api/player/{player_tag}
    path_parts = req.path.split('/')

    if len(path_parts) < 4:
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'Player tag is required'}),
            status=400,
            headers={'Content-Type': 'application/json'}
        )

    player_tag = path_parts[3]  # /api/player/{player_tag}

    # Fetch from Clash Royale API
    result = cr_api.get_player(player_tag)

    if not result['success']:
        return https_fn.Response(
            json.dumps(result),
            status=400,
            headers={'Content-Type': 'application/json'}
        )

    player_data = result['data']

    # Save to Firestore
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

    response_data = {
        'success': True,
        'player': player_data,
        'trends': trends,
        'roasts': roasts,
        'performance_emoji': performance_emoji,
        'skill_rating': skill_rating
    }

    return https_fn.Response(
        json.dumps(response_data),
        status=200,
        headers={'Content-Type': 'application/json'}
    )


@https_fn.on_request(cors=cors_options)
def get_player_history(req: https_fn.Request) -> https_fn.Response:
    """Get historical stats for a player

    Route: /api/player/<player_tag>/history
    Method: GET
    Query params: limit (int, default 30)
    """
    path_parts = req.path.split('/')

    if len(path_parts) < 4:
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'Player tag is required'}),
            status=400,
            headers={'Content-Type': 'application/json'}
        )

    player_tag = path_parts[3]
    limit = int(req.args.get('limit', 30))

    history = data_store.get_player_history(player_tag, limit=limit)

    if not history:
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'No historical data found'}),
            status=404,
            headers={'Content-Type': 'application/json'}
        )

    return https_fn.Response(
        json.dumps({'success': True, 'history': history}),
        status=200,
        headers={'Content-Type': 'application/json'}
    )


@https_fn.on_request(cors=cors_options)
def get_all_cards(req: https_fn.Request) -> https_fn.Response:
    """Get all unique cards with kiss counts

    Route: /api/cards
    Method: GET
    """
    cards = get_all_unique_cards()

    # Add kiss counts to each card
    for card in cards:
        card['kisses'] = kiss_tracker.get_card_kisses(card['name'])

    return https_fn.Response(
        json.dumps({'success': True, 'cards': cards}),
        status=200,
        headers={'Content-Type': 'application/json'}
    )


@https_fn.on_request(cors=cors_options)
def kiss_card(req: https_fn.Request) -> https_fn.Response:
    """Add a kiss to a card

    Route: /api/cards/kiss
    Method: POST
    Body: { "card_name": "Knight" }
    """
    if req.method != 'POST':
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'Method not allowed'}),
            status=405,
            headers={'Content-Type': 'application/json'}
        )

    try:
        data = req.get_json()
    except:
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'Invalid JSON'}),
            status=400,
            headers={'Content-Type': 'application/json'}
        )

    card_name = data.get('card_name')

    if not card_name:
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'card_name is required'}),
            status=400,
            headers={'Content-Type': 'application/json'}
        )

    new_count = kiss_tracker.add_kiss(card_name)

    return https_fn.Response(
        json.dumps({
            'success': True,
            'card_name': card_name,
            'kisses': new_count
        }),
        status=200,
        headers={'Content-Type': 'application/json'}
    )


@https_fn.on_request(cors=cors_options)
def slap_card(req: https_fn.Request) -> https_fn.Response:
    """Remove a kiss from a card (slap)

    Route: /api/cards/slap
    Method: POST
    Body: { "card_name": "Knight" }
    """
    if req.method != 'POST':
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'Method not allowed'}),
            status=405,
            headers={'Content-Type': 'application/json'}
        )

    try:
        data = req.get_json()
    except:
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'Invalid JSON'}),
            status=400,
            headers={'Content-Type': 'application/json'}
        )

    card_name = data.get('card_name')

    if not card_name:
        return https_fn.Response(
            json.dumps({'success': False, 'error': 'card_name is required'}),
            status=400,
            headers={'Content-Type': 'application/json'}
        )

    new_count = kiss_tracker.remove_kiss(card_name)

    return https_fn.Response(
        json.dumps({
            'success': True,
            'card_name': card_name,
            'kisses': new_count
        }),
        status=200,
        headers={'Content-Type': 'application/json'}
    )


@https_fn.on_request(cors=cors_options)
def get_kiss_leaderboard(req: https_fn.Request) -> https_fn.Response:
    """Get kiss leaderboard with card images

    Route: /api/cards/leaderboard
    Method: GET
    Query params: limit (int, default 50)
    """
    limit = int(req.args.get('limit', 50))
    leaderboard = kiss_tracker.get_leaderboard(limit=limit)

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

    return https_fn.Response(
        json.dumps({'success': True, 'leaderboard': leaderboard_with_images}),
        status=200,
        headers={'Content-Type': 'application/json'}
    )
