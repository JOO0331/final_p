#pip install -q -U sentence-transformers

import requests
import time
import json

def get_reviews(appid, params):
    url = f"https://store.steampowered.com/appreviews/{appid}"
    response = requests.get(url, params=params)
    return response.json()

def get_n_reviews(appid, n=100):
    reviews = []
    cursor = '*'
    num_per_page = 100  # 한 번에 가져올 리뷰 수

    while len(reviews) < n:
        params = {
            'json': 1,
            'language': 'korean',  # 한국어 리뷰
            'review_type': 'all',   # 모든 리뷰
            'purchase_type': 'all',  # 모든 구매 유형
            'cursor': cursor,
            'num_per_page': num_per_page
        }

        time.sleep(2)  # API 호출 간 대기 시간
        data = get_reviews(appid, params)

        if 'reviews' in data:
            reviews.extend(data['reviews'])
            cursor = data.get('cursor', None)
            if len(data['reviews']) < num_per_page:
                break  # 더 이상 리뷰가 없으면 종료
        else:
            print("리뷰를 가져오는 중 오류 발생:", data)
            break

    return reviews[:n]  # 요청한 수만큼 반환

def save_reviews_to_file(reviews, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

# 엘든 링의 앱 ID
appid = 1245620  # 엘든 링의 실제 앱 ID
reviews = get_n_reviews(appid, n=1000)  # 1000개의 리뷰를 가져옵니다

# 리뷰를 파일로 저장
save_reviews_to_file(reviews, 'elden_ring_reviews.json')
print(f"{len(reviews)}개의 리뷰가 'elden_ring_reviews.json' 파일에 저장되었습니다.")
