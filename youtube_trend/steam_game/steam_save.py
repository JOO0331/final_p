import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_trend.settings')
django.setup()
from steam_game.models import Game, GameReview
from datetime import datetime
import requests
import json

def load_steam_app_list():
    with open('steam_game/steam_app_list_2.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def get_game_tags(app_id):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={app_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tags = data.get('tags', [])
        if tags == []:
            return None
        else:
            tag_names = list(tags.keys())
            return tag_names
    else:
        print("Error fetching data from SteamSpy")
        return None

def fetch_and_save_games():
    apps = load_steam_app_list()
    
    for app in apps[:20]:
        app_id = app['appid']
        details_url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'

        details_response = requests.get(details_url)
        if details_response.status_code == 200:
            data = details_response.json()
            if str(app_id) in data and data[str(app_id)]['success']:
                game_data = data[str(app_id)]['data']

                tags = get_game_tags(app_id)
                tags_string = ', '.join(tags) if tags else ''

                price = game_data.get('price_overview', {})
                if price:
                    price_float = float(price.get('final_formatted', '').replace('₩', '').replace(',', '').strip())
                else:
                    price_float = 0

                game, created = Game.objects.update_or_create(
                    app_id=app_id,
                    defaults={
                        'name': game_data.get('name', ''),
                        'header_image': game_data.get('header_image', ''),
                        'release_date': datetime.strptime(game_data['release_date']['date'], '%d %b, %Y').date() if game_data.get('release_date', {}).get('date') else None,
                        'developers': ', '.join(game_data.get('developers', [])),
                        'publishers': ', '.join(game_data.get('publishers', [])),
                        'tags': tags_string,
                        'price': price_float,
                        'discount_percent': game_data.get('price_overview', {}).get('discount_percent', 0),
                        'supported_languages': game_data.get('supported_languages', ''),
                        'description': game_data.get('detailed_description', ''),
                        'review_summary': game_data.get('recommendations', {}).get('total', 'No reviews')
                    }
                )
                
                fetch_and_save_game_reviews(game)

def fetch_and_save_game_reviews(game):
    reviews_url = f'https://store.steampowered.com/appreviews/{game.app_id}?json=1'
    reviews_response = requests.get(reviews_url)
    
    if reviews_response.status_code == 200:
        reviews_data = reviews_response.json()
        for review in reviews_data.get('reviews', [])[:5]:
            GameReview.objects.update_or_create(
                game=game,
                review_id=review['recommendationid'],
                defaults={
                    'author': review['author']['steamid'],
                    'review_text': review['review'],
                    'is_positive': review['voted_up'],
                    'votes_helpful': review['votes_up'],
                    'created_at': datetime.fromtimestamp(review['timestamp_created'])
                }
            )


fetch_and_save_games()