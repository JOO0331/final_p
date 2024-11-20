"""
URL configuration for youtube_trend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from videos import views as video_views
from steam_game import views as steam_game_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", steam_game_views.game_list, name="game_list"),
    path("<int:app_id>/", steam_game_views.game_detail, name="game_detail"),
]
