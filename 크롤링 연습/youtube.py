# pip install --upgrade google-api-python-client
# pip install --upgrade google-auth-oauthlib google-auth-httplib2
from googleapiclient.discovery import build
import pandas as pd
import time
import schedule

def youtube_api():
    today=time.strftime('%Y-%m-%d %I %p', time.localtime(time.time()))
    now = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(time.time()))

    DEVELOPER_KEY = "요기다가 발급받은 키값"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    response = youtube.videos().list(
        maxResults = 20, # 최대 50까지 인듯
        part = "snippet, contentDetails, statistics",
        chart = "mostPopular",
        regionCode = "kr"
    ).execute()

    id = []
    pdate = []
    title = []
    channel = []
    category = []
    duration = []
    quality = []
    licensed = []
    view = []
    like = []
    dislike = []
    comment = []
    collectime = []

    for r in response['items']:
        id.append('https://www.youtube.com/watch?v=' + r['id'])
        pdate.append(r['snippet']['publishedAt'])
        title.append(r['snippet']['title'])
        channel.append(r['snippet']['channelTitle'])
        category.append(r['snippet']['categoryId'])
        duration.append(r['contentDetails']['duration'])
        quality.append(r['contentDetails']['definition'])
        licensed.append(r['contentDetails']['licensedContent'])
        view.append(r['statistics']['viewCount'])

        try:
            like.append(r['statistics']['likeCount'])
        except:
            like.append('None')
        try:
            dislike.append(r['statistics']['dislikeCount'])
        except:
            dislike.append('None')
        try:
            comment.append(r['statistics']['commentCount'])
        except:
            comment.append('None')
        collectime.append(now)

    df = pd.DataFrame({'published date':pdate, 'contents title':title, 'channel title':channel, 'category ID':category,
                     'duration':duration, 'video quality':quality, 'licensed':licensed, 'view':view, 'like':like,
                     'dislike':dislike, 'comment':comment, 'url':id, 'collect time':collectime})


    df.to_excel('요기다가 엑셀 파일 저장 경로')
    print(f'Collection success at {now}')

schedule.every().day.at("요기다가 크롤링 할 시간").do(youtube_api) # 없으니까 실행안됨

while True:
    schedule.run_pending()
    time.sleep(5)