import google.generativeai as genai

# https://aistudio.google.com/app/apikey?hl=ko 에서 API KEY 발급하여 사용

# API 키 설정
api_key = "AIzaSyCepvS94uzGYtFB_8Gq-zlXv2WGkMknmiw"
genai.configure(api_key=api_key)
youtube_url = "https://www.youtube.com/watch?v=Wx505sAnq98&t=12s"  # 유튜브 링크 입력

# 프롬프트 설정
prompt = f"이 유튜브 url은 게임리뷰 영상이야. 이 내용을 요약해서 게임 구매를 고민하는 사람에게 적절한 정보를 5줄~7줄로 내용을 정리해줘.\n내용 : {youtube_url}"
model = genai.GenerativeModel('gemini-pro')

try:
    # 콘텐츠 생성 요청
    response = model.generate_content(prompt)
    print(response.text, flush=True)  # 응답 출력
except Exception as e:
    # 오류 메시지 출력
    print(f"gRPC 호출 중 오류 발생")
