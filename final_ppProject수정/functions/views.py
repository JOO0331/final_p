from django.shortcuts import render
from .models import Game

def main_view(request):
    games = Game.objects.all()
    for game in games:
        game.final_price_int = int(float(str(game.final_price)))
        game.initial_price_int = int(float(str(game.initial_price)))
    return render(request, "main_gpt.html", {'games': games})

def search_view(request):
    games = Game.objects.all()
    return render(request, "search_gpt.html", {'games': games})

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