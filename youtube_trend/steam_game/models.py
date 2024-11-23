from django.db import models

class Game(models.Model):
    app_id = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    short_description = models.TextField()
    header_image = models.URLField()
    capsule_image = models.URLField()
    release_date = models.DateField(null=True)
    quarter = models.CharField(max_length=10, null=True, default=None)
    coming_soon = models.BooleanField(default=False)
    developers = models.CharField(max_length=500)
    publishers = models.CharField(max_length=500)
    tags = models.CharField(max_length=500)
    positive_reviews = models.IntegerField(default=0)
    negative_reviews = models.IntegerField(default=0)
    supported_languages = models.TextField()
    pc_requirements = models.JSONField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount_percent = models.IntegerField(default=0)
    categories = models.JSONField()
    genres = models.JSONField()
    screenshots = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['app_id', 'name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

class GameReview(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    review_id = models.CharField(max_length=100, db_index=True)
    review_text = models.TextField()
    updated_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['game', 'review_id']),
            models.Index(fields=['game', 'created_at']),
            models.Index(fields=['game', 'updated_at']),
        ]

    def __str__(self):
        return f"Review {self.review_id} for {self.game.name}"

class ReviewAnalysis(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='review_analysis')
    positive_keywords = models.JSONField()
    negative_keywords = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for {self.game.name}"

