import requests
import time
import json
import datetime

# 하단에 appid 와 max_reviews(최대리뷰수)를 입력
# 실행시 리뷰 데이터는 json 형식으로 appid_reivews_20241116 형태로 저장
# 이미지는 jpg파일로 appid_image.jpg 형태로 저장


# Steam API에서 특정 앱의 리뷰 데이터를 가져오기
def get_reviews(appid, params):
    url = f"https://store.steampowered.com/appreviews/{appid}" # 리뷰를 가져오는 API URL
    response = requests.get(url, params=params) # GET 요청으로 리뷰 데이터 요청
    # params (dict): API 요청에 필요한 파라미터.
    return response.json() # JSON 형식으로 반환


def get_korean_reviews(appid, max_reviews=1000):
    reviews = []  # 한국어 리뷰를 저장할 리스트
    cursor = '*'  # 초기 cursor 값
    num_per_page = 100  # 한 번에 가져올 리뷰 수 (스팀 API 최대값 : 100)

    while len(reviews) < max_reviews:
        params = {
            'json': 1,
            'language': 'korean',  # 한국어 리뷰만 가져오기
            'review_type': 'all',  # 모든 리뷰 (긍정, 부정 포함)
            'purchase_type': 'all',  # 모든 구매 유형 포함
            'cursor': cursor,
            'num_per_page': num_per_page,
            'day_range': 3650   #10년치 리뷰 가져오기(설정 안하면 최근 데이터만 가져오는 것 같아서 리뷰수가 적어짐)
        }

        time.sleep(2)  # API 호출 간 대기 시간(속도 제한 방지)
        data = get_reviews(appid, params) # API 호출

        # 가져온 리뷰 데이터가 유효한지 확인
        # 한 페이지에 100개의 리뷰만 확인 가능하므로 여러 페이지를 이동하면서 리뷰를 가져와야 함
        if 'reviews' in data and data['reviews']:  # 가져온 data에 reviews가 있는지 확인
            new_reviews = data['reviews']  # 새로 가져온 리뷰 리스트
            reviews.extend(new_reviews)  # 리뷰 리스트에 추가
            cursor = data.get('cursor', None)  # 다음 페이지로 이동할 커서 값 갱신
            print(f"{len(new_reviews)}개의 리뷰를 가져왔습니다. 총 {len(reviews)}개의 리뷰 저장 중...")

            # 가져온 리뷰가 num_per_page보다 적거나 커서가 없으면 더 이상 데이터가 없으므로 종료
            if len(new_reviews) < num_per_page or cursor is None:
                print("모든 리뷰를 가져왔습니다.")
                break
        else:
            # API 응답에서 리뷰를 가져오지 못한 경우
            print("리뷰를 가져오는 중 오류가 발생했거나 더 이상 리뷰가 없습니다.")
            break

        return reviews[:max_reviews]  # 요청한 최대 리뷰 수만 반환

# 게임 이미지 가져오기
def get_game_image(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url) # GET 요청으로 앱 데이터 요청
    data = response.json() # JSON 형식으로 반환

    # API 응답에서 성공적으로 데이터를 가져온 경우
    if str(appid) in data and data[str(appid)]['success']: # appid가 data에 포함되어 있고, success 값이 True일 때만
        game_data = data[str(appid)]['data']  # 게임 데이터
        image_url = game_data.get('header_image', None)  # 대표 이미지가 있는 URL를 header_image 필드에서 추출
        return image_url
    else:
        print("게임 이미지 정보를 가져오는 데 실패했습니다.")
        return None    # 실패 시 None 반환


# 이미지 저장
def save_image(image_url, filename):
    response = requests.get(image_url, stream=True) # 스트리밍 방식 사용: 메모리 사용량을 위해 데이터를 한번에 가져오는 대신 작은 청크 데이터로 처리
    if response.status_code == 200:  # 200이 성공
        with open(filename, 'wb') as f:   # 이미지는 바이너리(wb)로 저장
            for chunk in response.iter_content(1024): # 응답 데이터를 1kb(1024 바이트)씩 읽어 저장
                f.write(chunk) # 읽어온 데이터 청크를 파일에 기록
        print(f"이미지가 {filename}에 저장되었습니다.")
    else:
        print("이미지 다운로드에 실패했습니다.")


# 리뷰를 JSON 파일로 저장
def save_reviews_to_file(reviews, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)
        # json 파일 저장. ensure_ascii=False : 유니코드가 아닌 원래 문자(한글)로 표현, indent=4 : 가독성을 위한 들여쓰기)


# 통합 실행
if __name__ == "__main__":
    appid = 1245620  # 엘든 링의 실제 앱 ID
    max_reviews = 1000  # 가져올 리뷰 수 제한
    current_date = datetime.datetime.now().strftime("%Y%m%d")  # 현재 날짜를 '연월일' 형식으로 가져오기

    # 한국어 리뷰 가져오기
    korean_reviews = get_korean_reviews(appid, max_reviews=max_reviews)
    print(f"총 {len(korean_reviews)}개의 한국어 리뷰를 가져왔습니다.")

    # 리뷰를 파일로 저장
    reviews_filename = f"{appid}_reviews_{current_date}.json"  # ex: 1245620_reviews_20241116.json
    save_reviews_to_file(korean_reviews, reviews_filename)
    print(f"'{reviews_filename}' 파일에 리뷰가 저장되었습니다.")

    # 게임 이미지 가져오기 및 저장
    image_url = get_game_image(appid)
    if image_url:
        print(f"게임 이미지 URL: {image_url}")
        save_image(image_url, f"{appid}_image.jpg")