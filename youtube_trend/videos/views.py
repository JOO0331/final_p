from django.shortcuts import render
from .get_youtube import get_trending_videos


def video_list(request):
    videos = get_trending_videos()
    return render(request, "videos/video_list.html", {"videos": videos})
