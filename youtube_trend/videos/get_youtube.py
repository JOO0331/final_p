from googleapiclient.discovery import build
from django.conf import settings
from .models import Video
from django.core.cache import cache
from django.utils.dateparse import parse_datetime

def get_trending_videos():
    cached_videos = cache.get('trending_videos')
    if cached_videos is not None:
        return cached_videos

    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    
    request = youtube.videos().list(
        part='snippet,statistics',
        chart='mostPopular',
        regionCode='KR',
        maxResults=20
    )
    response = request.execute()

    Video.objects.all().delete()

    videos = []
    for item in response['items']:
        published_at = parse_datetime(item['snippet']['publishedAt'])
        
        video = Video.objects.create(
            video_id=item['id'],
            title=item['snippet']['title'],
            channel_title=item['snippet']['channelTitle'],
            thumbnail_url=item['snippet']['thumbnails']['high']['url'],
            view_count=int(item['statistics']['viewCount']),
            published_at=published_at
        )
        videos.append(video)

    cache.set('trending_videos', videos, 60 * 60)

    return videos