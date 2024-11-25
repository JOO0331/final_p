import json
import os

# 파일 경로 설정
file_path = "game_reviews.json"

# 중복 여부 확인 함수
def check_duplicate_reviews(file_path):
    if not os.path.exists(file_path):
        print(f"{file_path} 파일이 존재하지 않습니다.")
        return

    try:
        # JSON 데이터 로드
        with open(file_path, "r", encoding="utf-8") as json_file:
            reviews = json.load(json_file)

        # 중복 확인을 위한 세트
        seen_ids = set()
        duplicate_ids = set()

        for review in reviews:
            review_id = review.get("review_id")
            if review_id in seen_ids:
                duplicate_ids.add(review_id)
            else:
                seen_ids.add(review_id)

        # 결과 출력
        if duplicate_ids:
            print("중복된 review_id가 발견되었습니다:")
            print(duplicate_ids)
        else:
            print("중복된 review_id가 없습니다.")
    except Exception as e:
        print(f"JSON 파일 처리 중 오류 발생: {e}")

# 중복 여부 확인 실행
check_duplicate_reviews(file_path)
