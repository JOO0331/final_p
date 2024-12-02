
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_view, name="main"),
    path('search/', views.search_view, name="search"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
]
