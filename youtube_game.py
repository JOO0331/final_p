import requests

# API 키와 영상 ID 설정
api_key = '유튜브 api'
video_id = 'ESrJX0OIIwc'

# API 호출 URL 설정 (liveBroadcastContent 파라미터 제거)
url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'

# API 호출
response = requests.get(url)

# 응답 상태 코드 확인
if response.status_code == 200:
    video_data = response.json()


    # 영상의 메타데이터에서 정보 추출
    if 'items' in video_data:
        video_info = video_data['items'][0]['snippet']
        print(f"Title: {video_info['title']}")
        print(f"Description: {video_info['description']}")
        print(f"Category ID: {video_info['categoryId']}")  # 게임 관련 카테고리 ID

        # 'tags'가 있을 경우 출력
        print(f"Tags: {video_info.get('tags', 'No tags available')}")

        # 게임 ID (이 값이 존재하면 게임 이름도 함께 제공됨)
        if 'gameId' in video_info:
            game_id = video_info['gameId']
            print(f"Game ID: {game_id}")

            # 게임 ID로 게임 이름을 가져오는 추가 API 호출
            game_url = f'https://www.googleapis.com/youtube/v3/games?part=snippet&id={game_id}&key={api_key}'
            game_response = requests.get(game_url)
            if game_response.status_code == 200:
                game_data = game_response.json()
                if 'items' in game_data:
                    game_name = game_data['items'][0]['snippet']['title']
                    print(f"Game Name: {game_name}")
                else:
                    print("Game name not found.")
            else:
                print("Error fetching game details.")
        else:
            print("No game ID associated with this video.")
    else:
        print("No video found with the given ID.")
else:
    print(f"API call failed with status code {response.status_code}.")
    print(f"Error response: {response.text}")