import os
import django
import sys
import requests
import json
import time
from datetime import datetime
from django.utils import timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_trend.settings')
django.setup()

from steam_game.models import Game, GameReview

output_file_path = 'output.txt'
output_file = open(output_file_path, 'w', encoding='utf-8')

def print_to_file(message):
    print(message)
    output_file.write(message + '\n')

def load_steam_tag_top100():
    with open('game_list/top100in2weeks.json', 'r', encoding='utf-8') as f:
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
        print_to_file("SteamSpy에서 tag 가져오기 실패")
        return None

def fetch_and_save_games_indie():
    apps = load_steam_tag_top100()
    
    for app in apps:
        app_id = app['app_id']
        details_url = f'https://store.steampowered.com/api/appdetails?appids={app_id}&cc=KR'

        try:
            details_response = requests.get(details_url)
            details_response.raise_for_status()
            
            data = details_response.json()
            if str(app_id) in data and data[str(app_id)]['success']:
                game_data = data[str(app_id)]['data']
                
                if game_data.get('type') != 'game':
                    continue

                tags = get_game_tags(app_id)
                tags_string = ', '.join(tags) if tags else ''


                price_info = game_data.get('price_overview', {})
                initial_price = float(price_info.get('initial', 0)) / 100 if price_info else 0
                final_price = float(price_info.get('final_formatted', '').replace('₩', '').replace(',', '').strip()) if price_info else 0
                discount_percent = price_info.get('discount_percent', 0)

                release_date = game_data.get('release_date', {})
                coming_soon = release_date.get('coming_soon', False)
                if not coming_soon:
                    release_date_str = release_date.get('date')
                    
                    if release_date_str:
                        try:
                            release_date_obj = datetime.strptime(release_date_str, '%d %b, %Y').date()
                        except ValueError:
                            release_date_obj = datetime.strptime(release_date_str, '%b %Y').date()
                    else:
                        release_date_obj = None

                    release_date_quarter = None
                else:
                    release_date_obj = None
                    release_date_quarter = release_date.get('date')

                game, created = Game.objects.update_or_create(
                    app_id=app_id,
                    defaults={
                        'name': game_data.get('name', ''),
                        'header_image': game_data.get('header_image', ''),
                        'capsule_image': game_data.get('capsule_image', ''),
                        'release_date': release_date_obj,
                        'coming_soon': release_date.get('coming_soon', False),
                        'quarter': release_date_quarter,
                        'developers': ', '.join(game_data.get('developers', [])),
                        'publishers': ', '.join(game_data.get('publishers', [])),
                        'supported_languages': game_data.get('supported_languages', ''),
                        'short_description': game_data.get('short_description', ''),
                        'tags': tags_string,
                        'positive_reviews': app['positive'],
                        'negative_reviews': app['negative'],
                        'pc_requirements': game_data.get('pc_requirements', {}),
                        'initial_price': initial_price,
                        'final_price': final_price,
                        'discount_percent': discount_percent,
                        'categories': game_data.get('categories', []),
                        'genres': game_data.get('genres', []),
                        'screenshots': game_data.get('screenshots', [])
                    }
                )
                
                print_to_file(f"게임 {game.name} 저장 완료")
                fetch_and_save_game_reviews(game)
                time.sleep(1)

        except requests.exceptions.RequestException as e:
            print_to_file(f"게임 정보 가져오기 실패 (ID: {app_id}): {e}")
            time.sleep(5)
            continue
        
        except Exception as e:
            print_to_file(f"예상치 못한 오류 발생 (ID: {app_id}): {e}")
            continue

def fetch_and_save_game_reviews(game, total_reviews=1000):
    cursor = '*'
    count = 100
    batch_count = 0
    processed_reviews = 0
    
    print_to_file(f"게임 {game.name}({game.app_id})의 리뷰 수집 시작")

    while processed_reviews < total_reviews:
        reviews_url = (
            f'https://store.steampowered.com/appreviews/{game.app_id}'
            f'?json=1&cursor={requests.utils.quote(cursor)}&num_per_page={count}&language=koreana'
            f'&filter=updated&review_type=all&purchase_type=all'
        )
        
        try:
            response = requests.get(reviews_url)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                print_to_file("API 응답 실패")
                break

            reviews = data.get('reviews', [])
            if not reviews:
                print_to_file("리뷰가 비어서 다음페이지로 넘어갑니다")
                new_cursor = data.get('cursor')
                if not new_cursor or new_cursor == cursor:
                    print_to_file("리뷰가 비었고 더 이상 새로운 페이지가 없습니다")
                    break
                cursor = new_cursor
                continue

            new_reviews_in_batch = 0
            print_to_file(f"API에서 받은 리뷰 수: {len(reviews)}")
            
            for review in reviews:
                try:
                    review_id = review.get('recommendationid')
                    review_text = review.get('review')
                    timestamp = review.get('timestamp_updated')
                    
                    if not review_text.strip():
                        continue
                        
                    GameReview.objects.update_or_create(
                        game=game,
                        review_id=review_id,
                        defaults={
                            'review_text': review_text,
                            'updated_at': timezone.make_aware(datetime.fromtimestamp(timestamp))
                        }
                    )
                    processed_reviews += 1
                    new_reviews_in_batch += 1
                    
                except Exception as e:
                    print_to_file(f"리뷰 저장 중 오류 발생: {e}")
                    continue

            print_to_file(f"이번 배치에서 처리된 리뷰 수: {new_reviews_in_batch}")
            print_to_file(f"현재까지 총 처리된 리뷰 수: {processed_reviews}")

            new_cursor = data.get('cursor')
            if not new_cursor or new_cursor == cursor:
                print_to_file("더 이상 새로운 페이지가 없습니다.")
                break
            cursor = new_cursor

            batch_count += 1
            if batch_count >= 5:  
                print_to_file("5번 수행 완료, 2초 대기...")
                time.sleep(2)
                batch_count = 0
            else:
                time.sleep(0.1)

        except requests.exceptions.RequestException as e:
            print_to_file(f"리뷰 가져오기 실패: {e}")
            time.sleep(5)
            continue
        
        except Exception as e:
            print_to_file(f"예상치 못한 오류 발생: {e}")
            print_to_file(f"Cursor 값: {cursor}")
            break

    print_to_file(f"최종 처리된 총 리뷰 수: {processed_reviews}")
    print_to_file(f"DB에 저장된 이 게임의 총 리뷰 수: {GameReview.objects.filter(game=game).count()}")

print_to_file(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
fetch_and_save_games_indie()
print_to_file(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
output_file.close()

