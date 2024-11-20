import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_trend.settings')
django.setup()
from datetime import datetime
import requests
import json

def load_steam_app_list():
    with open('steam_game/steam_app_list_2.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_games():
    apps = load_steam_app_list()
    all_game_data = []
    
    for app in apps[:20]:
        app_id = app['appid']
        details_url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
        details_response = requests.get(details_url)
        if details_response.status_code == 200:
            data = details_response.json()
            if str(app_id) in data and data[str(app_id)]['success']:
                game_data = data[str(app_id)]['data']
                all_game_data.append(game_data)
                
    with open('steam_game/game_list/saved_games.json', 'w', encoding='utf-8') as f:
        json.dump(all_game_data, f, ensure_ascii=False, indent=4)

def save_game_reviews(game):
    reviews_url = f'https://store.steampowered.com/appreviews/{game.app_id}?json=1'
    reviews_response = requests.get(reviews_url)
    
    if reviews_response.status_code == 200:
        reviews_data = reviews_response.json()
        reviews_list = [] 

        for review in reviews_data.get('reviews', [])[:5]:
            reviews_list.append({
                'author': review['author']['steamid'],
                'review_text': review['review'],
                'is_positive': review['voted_up'],
                'votes_helpful': review['votes_up'],
                'created_at': datetime.fromtimestamp(review['timestamp_created'])
            })

    with open(f'steam_game/game_list/reviews/reviews_{game.name}.json', 'w', encoding='utf-8') as f:
            json.dump(reviews_list, f, ensure_ascii=False, indent=4)


save_games()