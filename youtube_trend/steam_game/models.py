from django.db import models
from bson.decimal128 import Decimal128

class Game(models.Model):
    app_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    header_image = models.URLField()
    release_date = models.DateField(null=True)
    developers = models.CharField(max_length=500)
    publishers = models.CharField(max_length=500)
    tags = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount_percent = models.IntegerField(default=0)
    supported_languages = models.TextField()
    review_summary = models.CharField(max_length=100)
    positive_reviews = models.IntegerField(default=0)
    negative_reviews = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_final_price(self):
        if self.price:
            if isinstance(self.price, Decimal128):
                price_decimal = self.price.to_decimal()
            else:
                price_decimal = self.price
            return price_decimal
        return 0

class GameReview(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    review_id = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    review_text = models.TextField()
    is_positive = models.BooleanField()
    votes_helpful = models.IntegerField()
    created_at = models.DateTimeField()

