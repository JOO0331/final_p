import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_trend.settings')
django.setup()
import requests
import json

def fetch_steam_tag_indie():
    response = requests.get('https://steamspy.com/api.php?request=tag&tag=Indie')
    data = response.json()
    games = [{"app_id": app_id, "positive": game["positive"], "negative": game["negative"]} for app_id, game in data.items()]

    with open('game_list/steam_tag_indie.json', 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=4)

fetch_steam_tag_indie()