import pymongo
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import string

# 몽고디비 클라이언트 연결
client = pymongo.MongoClient("mongodb://localhost:27017/")  # 몽고디비 주소
db = client["steam_reviews"]  # 데이터베이스 이름
#collection = db["negative_reviews"]  # 컬렉션 이름
collection = db["positive_reviews"]

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

# TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=10, stop_words=stopwords, max_df=0.9, min_df=2)
X = vectorizer.fit_transform(review_texts)

# TF-IDF에서 가장 중요한 단어들 추출
feature_names = vectorizer.get_feature_names_out()
sorted_indices = X.sum(axis=0).A1.argsort()[::-1]  # TF-IDF 값이 높은 순으로 정렬

# 상위 10개 키워드 출력
print("가장 중요한 키워드 (TF-IDF):")
for idx in sorted_indices[:10]:
    tfidf_value = X.sum(axis=0).A1[idx]
    print(f"{feature_names[idx]}: {tfidf_value:.4f}")
