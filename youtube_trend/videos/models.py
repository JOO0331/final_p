from django.db import models

# Create your models here.

class Video(models.Model):
    video_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    channel_title = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    view_count = models.BigIntegerField()
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-view_count"]

    def __str__(self):
        return self.title

    def format_view_count(self):
        if self.view_count >= 100000000:
            return f"{self.view_count//100000000}억회"
        elif self.view_count >= 10000:
            return f"{self.view_count//10000}만회"
        elif self.view_count >= 1000:
            return f"{self.view_count//1000}천회"
        else:
            return f"{self.view_count}회"

    def format_published_time(self):
        return self.published_at.strftime("%Y.%m.%d")
