import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_trend.settings')
django.setup()
from datetime import datetime
import requests
import json

def save_games():
    korean_reviews = []
    cursor = 'AoJ47sHKupADfrvhPQ==' 
    count = 100
    
    app_id = '570'
    reviews_url = (
            f'https://store.steampowered.com/appreviews/{app_id}'
            f'?json=1&cursor={requests.utils.quote(cursor)}&num_per_page={count}&language=koreana'
            f'&filter=updated&review_type=all&purchase_type=all'
        )
    reviews_response = requests.get(reviews_url)
    if reviews_response.status_code == 200:
        review = reviews_response.json()
                
    with open('game_list/test_dota2_2.json', 'w', encoding='utf-8') as f:
        json.dump(review, f, ensure_ascii=False, indent=4)

def len_dota2_reviews():
    with open('game_list/test_dota2_2.json', 'r', encoding='utf-8') as f:
        review = json.load(f)
    print(len(review['reviews']))

save_games()
# len_dota2_reviews()