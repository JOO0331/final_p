import requests
import time
import json
import datetime


def get_game_image(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url) # GET 요청으로 앱 데이터 요청
    data = response.json() # JSON 형식으로 반환
    save_reviews_to_file(data, f"{appid}_크롤링가능데이터.json")

def save_reviews_to_file(reviews, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)
        # json 파일 저장. ensure_ascii=False : 유니코드가 아닌 원래 문자(한글)로 표현, indent=4 : 가독성을 위한 들여쓰기)

if __name__ == '__main__':
    get_game_image(1245620)