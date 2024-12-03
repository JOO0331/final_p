import pymongo
from konlpy.tag import Okt
from bertopic import BERTopic
import string
from sentence_transformers import SentenceTransformer

# 몽고디비 클라이언트 연결
client = pymongo.MongoClient("mongodb://localhost:27017/")  # 몽고디비 주소
db = client["steam_reviews"]  # 데이터베이스 이름
#collection = db["positive_reviews"]  # 컬렉션 이름
collection = db["negative_reviews"]

# 리뷰 데이터 불러오기
reviews = collection.find()  # 모든 리뷰 데이터 가져오기

# Okt 형태소 분석기 사용
okt = Okt()

# 불용어 리스트 (예시)
stopwords = ['게임', '언제', '이다', '아시', '진짜', '그냥', '핑좀',  '병신', '시발', '제발', '추천','도', '는', '다', '의', '가',
             '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지','임', '게', '만',
             '겜', '되', '음', '면', '파', '도', '발', '비', '개', '좀', '왜', '더', '것', '준', '민', '수', '내', '나', '그',
             '함', '때', '정말']

# 텍스트 전처리 함수
def preprocess_text(text):
    # 텍스트 소문자로 변환 (한국어에는 불필요할 수 있음)
    text = text.lower()
    # 구두점 (.,?!;:)제거
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 명사만 추출
    nouns = okt.nouns(text)
    # 불용어 제거
    nouns = [noun for noun in nouns if noun not in stopwords]
    return ' '.join(nouns)

# 모든 리뷰에서 키워드 추출
review_texts = []

for review in reviews:
    if 'review_text' in review:
        review_text = review['review_text']
        processed_text = preprocess_text(review_text)
        review_texts.append(processed_text)

# 리뷰 텍스트가 비어 있지 않은지 확인
if not review_texts:
    print("리뷰 텍스트가 비어 있습니다.")
    exit()

# SentenceTransformer 모델 생성
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') # 텍스트를 벡터 형태로 변환

# 리뷰 텍스트에서 임베딩 생성
embeddings = model.encode(review_texts, show_progress_bar=True)

# BERTopic 모델 생성
topic_model = BERTopic(language="multilingual")

# 모델에 데이터 적용하여 토픽 추출 (임베딩을 수동으로 전달)
topics, probabilities = topic_model.fit_transform(review_texts, embeddings)

# 토픽 추출 결과 확인
print("가장 중요한 토픽들:")
# 상위 10개의 토픽만 출력
for i in range(min(10, len(set(topics)))):
    print(f"토픽 {i}: {topic_model.get_topic(i)}")

# 토픽 0: 게임 관련 불만 및 시스템 관련
# 토픽 1: 게임의 장점과 긍정적인 측면
# 토픽 2: 서버와 관리 문제
# 토픽 3: 부정적인 표현과 불만
# 토픽 4: 게임에 대한 부정적인 반응
# 토픽 5: 또 다른 강한 부정적 감정