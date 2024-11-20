import requests


def get_game_tags(app_id):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={app_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        tags = data.get('tags', [])
        return tags
    else:
        print("Error fetching data from SteamSpy")
        return None

app_id = 1532770


tags = get_game_tags(app_id)

if tags is not None:
    print(f"Korean Tags for app_id {app_id}: {tags}")