from django.shortcuts import render
from .models import Game

def main_view(request):
    return render(request, "main_gpt.html")

def search_view(request):
    return render(request, "search_gpt.html")

def dashboard_view(request):
    game = Game.objects.get(app_id=105600)
    return render(request, 'dash_gpt.html', {'game': game})


# Create your views here.
# def index(request):
#     context = {
#         "title": "My Site",
#         "site_name": "Django Template Example",
#         "items": ["Item 1", "Item 2", "Item 3"]
#     }
#     return render(request, "main_gpt.html", context)