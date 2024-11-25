import os
import aiohttp
import asyncio
import json
import ctypes
from datetime import datetime, timezone
from dateutil import parser  # 날짜 파싱을 위한 라이브러리

# 출력 파일 설정
output_file_path = 'output.txt'
output_file = open(output_file_path, 'a', encoding='utf-8')

# 로그 메시지를 출력 및 파일에 기록하는 함수
def print_to_file(message):
    print(message)
    output_file.write(message + '\n')

# Steam 인기 게임 목록 파일 로드
def load_steam_tag_top100():
    with open('top100in2weeks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # app_id를 키로 하는 딕셔너리 생성
    return {int(app['app_id']): app for app in data}

# 기존 JSON 데이터 로드
def load_existing_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return {}

# JSON 데이터 저장
def save_json(file_path, data):
    if os.path.exists(file_path):
        remove_readonly(file_path)  # 읽기 전용 속성 해제
    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print_to_file(f"JSON 데이터 저장 완료: {file_path}")
    except Exception as e:
        print_to_file(f"JSON 데이터 저장 중 오류 발생: {e}")

# 읽기 전용 속성 제거 함수
def remove_readonly(file_path):
    try:
        FILE_ATTRIBUTE_READONLY = 0x01
        attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
        if attrs & FILE_ATTRIBUTE_READONLY:
            ctypes.windll.kernel32.SetFileAttributesW(file_path, attrs & ~FILE_ATTRIBUTE_READONLY)
        print_to_file(f"읽기 전용 속성 제거 성공: {file_path}")
    except Exception as e:
        print_to_file(f"읽기 전용 속성 제거 실패: {e}")
# 비동기적으로 게임 태그를 가져오는 함수(steamspy)
async def get_game_tags(session, app_id):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={app_id}"
    async with session.get(url) as response:
        if response.status == 200:  # API 요청 성공
            data = await response.json()
            tags = data.get('tags', [])
            return list(tags.keys()) if tags else []
        else:
            print_to_file(f"SteamSpy에서 tag 가져오기 실패 (ID: {app_id})")
            return []

# 게임 정보를 가져오는 함수
async def fetch_game_metadata(session, app_id, app_data):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=korean"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if str(app_id) in data and data[str(app_id)]['success']:
                    game_data = data[str(app_id)]['data']
                    release_date_info = game_data.get("release_date", {})
                    date_str = release_date_info.get("date", "N/A")
                    try:
                        parsed_date = parser.parse(date_str, fuzzy=True)
                        month = parsed_date.month
                        quarter = f"Q{(month - 1) // 3 + 1}"
                    except (ValueError, IndexError, TypeError):
                        quarter = "N/A"

                    metadata = {
                        "app_id": app_id,
                        "name_kor": game_data.get("name", "N/A"),
                        "name_eng": game_data.get("name", "N/A"),
                        "short_description": game_data.get("short_description", "N/A"),
                        "capsule_image": game_data.get("capsule_image", "N/A"),
                        "header_image": game_data.get("header_image", "N/A"),
                        "release_date": date_str,
                        "quarter": quarter,
                        "coming_soon": release_date_info.get("coming_soon", False),
                        "developers": game_data.get("developers", []),
                        "publishers": game_data.get("publishers", []),
                        "tags": await get_game_tags(session, app_id),
                        "positive_reviews": app_data.get("positive", 0),
                        "negative_reviews": app_data.get("negative", 0),
                        "supported_languages": game_data.get("supported_languages", "N/A"),
                        "pc_requirements": game_data.get("pc_requirements", {}).get("minimum", "N/A"),
                        "discount_percent": game_data.get("price_overview", {}).get("discount_percent", 0),
                        "initial_price": game_data.get("price_overview", {}).get("initial", 0)/100,
                        "final_price": game_data.get("price_overview", {}).get("final", 0)/100,
                        "categories": game_data.get("categories", []),
                        "genres": game_data.get("genres", []),
                        "screenshots": game_data.get("screenshots", []),
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    }
                    print_to_file(f"게임 메타정보 저장 완료: {metadata['name_kor']} (ID: {app_id})")
                    return metadata
            else:
                print_to_file(f"Steam API 요청 실패 (ID: {app_id}, 상태 코드: {response.status})")
    except Exception as e:
        print_to_file(f"게임 메타정보 가져오기 실패 (ID: {app_id}): {e}")
    return None

# 리뷰 데이터를 가져오는 함수
async def fetch_game_reviews(session, app_id, game_name, max_reviews=20000):
    reviews = {}
    cursor = '*'
    num_per_page = 100
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    while len(reviews) < max_reviews:
        params = {
            'json': 1,
            'language': 'koreana',
            'review_type': 'all',
            'purchase_type': 'all',
            'cursor': cursor,
            'num_per_page': num_per_page,
            'day_range': 365
        }
        try:
            async with session.get(f"https://store.steampowered.com/appreviews/{app_id}", headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'reviews' in data and data['reviews']:
                        for review in data['reviews']:
                            review_id = review.get("recommendationid")
                            if review_id not in reviews:
                                reviews[review_id] = {
                                    "game": app_id,
                                    "review_id": review_id,
                                    "review_text": review.get("review", ""),
                                    "created_at": datetime.now(timezone.utc).isoformat(),
                                    "updated_at": datetime.fromtimestamp(review.get("timestamp_updated", 0), tz=timezone.utc).isoformat(),
                                }
                        cursor = data.get('cursor', None)
                        if len(data['reviews']) < num_per_page or not cursor:
                            break
                    else:
                        break
        except Exception as e:
            print_to_file(f"리뷰 가져오기 실패 (ID: {app_id}): {e}")
            break
        await asyncio.sleep(1)

    print_to_file(f"게임명 {game_name} (ID: {app_id}) 리뷰 수집 완료: 총 {len(reviews)}개")
    return reviews
async def fetch_and_save_games():
    start_time = datetime.now()
    apps = load_steam_tag_top100()
    existing_metadata = load_existing_json("game_metadata.json")
    existing_reviews = load_existing_json("game_reviews.json")

    all_games_metadata = existing_metadata.copy()
    all_reviews_data = {review["review_id"]: review for review in existing_reviews}  # Ensure it's a dict

    async with aiohttp.ClientSession() as session:
        # 게임 메타데이터 처리
        game_tasks = [
            fetch_game_metadata(session, app_id, app_data)
            for app_id, app_data in apps.items()
        ]
        games_metadata = await asyncio.gather(*game_tasks)

        # 메타데이터 병합
        for game_metadata in games_metadata:
            if game_metadata:
                all_games_metadata[str(game_metadata["app_id"])] = game_metadata

        # 리뷰 데이터 처리
        review_tasks = [
            fetch_game_reviews(session, game["app_id"], game["name_eng"])
            for game in games_metadata if game
        ]
        reviews_results = await asyncio.gather(*review_tasks)

        # 리뷰 데이터 병합
        for reviews in reviews_results:
            all_reviews_data.update(reviews)

    # JSON 파일로 저장
    save_json("game_metadata.json", all_games_metadata)
    save_json("game_reviews.json", list(all_reviews_data.values()))

    elapsed_time = datetime.now() - start_time
    print_to_file(f"\n총 저장된 게임 수: {len(all_games_metadata)}개")
    print_to_file(f"총 저장된 리뷰 수: {len(all_reviews_data)}개")
    print_to_file(f"총 걸린 시간: {elapsed_time}")

# 실행
print_to_file(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
asyncio.run(fetch_and_save_games())
print_to_file(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
output_file.close()
