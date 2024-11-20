from django.shortcuts import render, get_object_or_404
from .models import Game

def game_list(request):
    games = Game.objects.all()
    return render(request, "steam/game_list.html", {"games": games})

def game_detail(request, app_id):
    game = get_object_or_404(Game, app_id=app_id)
    return render(request, "steam/game_detail.html", {"game": game})
