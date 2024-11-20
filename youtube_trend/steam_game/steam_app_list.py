import requests
import json

def fetch_steam_app_list():
    response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    apps = response.json()['applist']['apps']

    with open('steam_app_list.json', 'w', encoding='utf-8') as f:
        json.dump(apps, f, ensure_ascii=False, indent=4)

def clean_steam_app_list():
    with open('steam_game/steam_app_list.json', 'r', encoding='utf-8') as f:
        apps = json.load(f)
    
    filtered_apps = [app for app in apps if app['name'].strip() != '']
    
    with open('steam_game/steam_app_list_2.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_apps, f, ensure_ascii=False, indent=4)
    
    print(f"원본 앱 수: {len(apps)}")
    print(f"필터링 후 앱 수: {len(filtered_apps)}")
    
    return filtered_apps

clean_steam_app_list()