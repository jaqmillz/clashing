"""Clash Royale API Client"""

import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote

# Load environment variables
load_dotenv()

class ClashRoyaleAPI:
    """Client for Clash Royale API"""

    BASE_URL = "https://api.clashroyale.com/v1"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('CLASH_ROYALE_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set CLASH_ROYALE_API_KEY in .env file")

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }

    def _encode_tag(self, tag):
        """Encode player tag for URL (handle # symbol)"""
        if not tag.startswith('#'):
            tag = f'#{tag}'
        return quote(tag)

    def get_player(self, player_tag):
        """Get player information by tag"""
        encoded_tag = self._encode_tag(player_tag)
        url = f"{self.BASE_URL}/players/{encoded_tag}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json()
            }
        except requests.exceptions.HTTPError as e:
            error_detail = ''
            try:
                error_detail = e.response.json().get('message', e.response.text)
            except:
                error_detail = e.response.text

            print(f"API Error {e.response.status_code}: {error_detail}")

            if e.response.status_code == 404:
                return {
                    'success': False,
                    'error': 'Player not found'
                }
            elif e.response.status_code == 403:
                return {
                    'success': False,
                    'error': f'Invalid API key or IP restricted: {error_detail}'
                }
            else:
                return {
                    'success': False,
                    'error': f'API error {e.response.status_code}: {error_detail}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_battlelog(self, player_tag):
        """Get player's recent battles"""
        encoded_tag = self._encode_tag(player_tag)
        url = f"{self.BASE_URL}/players/{encoded_tag}/battlelog"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_upcoming_chests(self, player_tag):
        """Get player's upcoming chests"""
        encoded_tag = self._encode_tag(player_tag)
        url = f"{self.BASE_URL}/players/{encoded_tag}/upcomingchests"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
