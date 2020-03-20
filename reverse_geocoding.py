import requests
import json

def get_area(lat,lon):
    url = "https://us1.locationiq.com/v1/reverse.php"

    data = {
        'key': '0ed244a8d1cf03',
        'lat': str(lat),
        'lon': str(lon),
        'format': 'json'
    }
    response = requests.get(url, params=data)
    data = json.loads(response.text)
    return data['display_name']

print(get_area(23,72))