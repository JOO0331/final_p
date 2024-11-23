import os
import django
import sys
import requests
import json
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_trend.settings')
django.setup()

def fetch_reviews(app_id, total_reviews=100):
    korean_reviews = []
    cursor = '*'
    count = 20
    
    print(f"게임 ID {app_id}의 리뷰 수집 시작")

    while len(korean_reviews) < total_reviews:
        reviews_url = (
            f'https://store.steampowered.com/appreviews/{app_id}'
            f'?json=1&cursor={cursor}&count={count}&language=koreana'
            f'&filter=all&review_type=all'
        )
        
        try:
            response = requests.get(reviews_url)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success') or not data.get('reviews'):
                print("더 이상 리뷰를 가져올 수 없습니다.")
                break

            cursor = data.get('cursor')
            
            new_reviews = data.get('reviews', [])
            print(f"가져온 리뷰 수: {len(new_reviews)}")
            
            for review in new_reviews:
                if review not in korean_reviews:
                    korean_reviews.append(review)
                    print(f"현재까지 수집된 총 한국어 리뷰 수: {len(korean_reviews)}")

            if not cursor or cursor == '*':
                print("모든 리뷰를 가져왔습니다.")
                break

            time.sleep(3)

        except requests.exceptions.RequestException as e:
            print(f"리뷰 가져오기 실패: {e}")
            time.sleep(5)
            continue
        
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
            break

    print(f"최종 수집된 한국어 리뷰 수: {len(korean_reviews)}")
    
    if korean_reviews:
        with open('game_list/reviews/korean_reviews.json', 'w', encoding='utf-8') as f:
            json.dump(korean_reviews, f, ensure_ascii=False, indent=4)
        print("리뷰가 파일에 저장되었습니다.")
    else:
        print("저장할 한국어 리뷰가 없습니다.")

    return len(korean_reviews)

total_reviews = fetch_reviews(578080)
print(f"총 수집된 리뷰 수: {total_reviews}")