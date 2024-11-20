import json
from transformers import pipeline, BertTokenizer, BertForSequenceClassification

# sentiment_analysis = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment") 정확도 매우 낮음

# tokenizer = BertTokenizer.from_pretrained('monologg/kobert', trust_remote_code=True)
# model = BertForSequenceClassification.from_pretrained('monologg/kobert', num_labels=3, trust_remote_code=True) 정확도 매우 낮음

tokenizer = BertTokenizer.from_pretrained('beomi/KcBERT-base', trust_remote_code=True)
model = BertForSequenceClassification.from_pretrained('beomi/KcBERT-base', num_labels=3, trust_remote_code=True)

sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

with open('test_review_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    text = item['review_text']
    result = sentiment_analysis(text)
    print(f"Text: {text}")
    print(f"Sentiment: {result[0]['label']}, Score: {result[0]['score']:.4f}")

# 5 stars(LABEL_4) : 매우 긍정적
# 4 stars(LABEL_3) : 긍정적
# 3 stars(LABEL_2) : 중립적 또는 보통
# 2 stars(LABEL_1) : 부정적
# 1 star(LABEL_0) : 매우 부정적
# (LABEL_0) : 부정적    
# (LABEL_1) : 중립적 또는 보통
# (LABEL_2) : 긍정적