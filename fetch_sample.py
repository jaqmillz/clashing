#!/usr/bin/env python3
"""Fetch and save sample API response"""
import json
from cr_api import ClashRoyaleAPI

cr_api = ClashRoyaleAPI()
result = cr_api.get_player('#JCJGLJ2Y')

if result['success']:
    with open('sample_player_response.json', 'w') as f:
        json.dump(result['data'], f, indent=2)
    print("✅ Sample response saved to sample_player_response.json")
    print(f"\n📊 Player: {result['data']['name']}")
    print(f"🏆 Trophies: {result['data']['trophies']:,}")
else:
    print(f"❌ Error: {result['error']}")
