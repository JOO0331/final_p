from django.shortcuts import render
from .models import Game
import re

def main_view(request):
    games = Game.objects.all()
    for game in games:
        game.final_price_int = int(float(str(game.final_price)))
        game.initial_price_int = int(float(str(game.initial_price)))
    return render(request, "main_gpt.html", {'games': games})

def search_view(request):
    query = request.GET.get('search', '')
    games = Game.objects.all()
    
    if query:
        games = games.filter(name__icontains=query)
    
    for game in games:
        game.final_price_int = int(float(str(game.final_price)))
        game.initial_price_int = int(float(str(game.initial_price)))
    
    return render(request, "search_gpt.html", {'games': games})

def dashboard_view(request, app_id):
    game = Game.objects.get(app_id=app_id)
    game.final_price_int = int(float(str(game.final_price)))
    game.initial_price_int = int(float(str(game.initial_price)))
    
    if isinstance(game.tags, str):
        game.tags = [tag.strip() for tag in game.tags.split(',')]
    
    if isinstance(game.supported_languages, str):
        clean_text = re.sub('<[^<]+?>', '', game.supported_languages)
        main_languages = clean_text.split('languages with full audio support')[0]
        languages = [lang.strip() for lang in main_languages.split(',')]
        game.supported_languages = [lang.replace('*', '').strip() for lang in languages]
    
    if isinstance(game.developers, str):
        game.developers = [dev.strip() for dev in game.developers.split(',')]
    
    if isinstance(game.publishers, str):
        game.publishers = [pub.strip() for pub in game.publishers.split(',')]
    
    return render(request, 'dash_gpt.html', {'game': game})


# Create your views here.
# def index(request):
#     context = {
#         "title": "My Site",
#         "site_name": "Django Template Example",
#         "items": ["Item 1", "Item 2", "Item 3"]
#     }
#     return render(request, "main_gpt.html", context)